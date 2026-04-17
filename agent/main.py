"""
LingXi Daily Agent — 主工作流编排

需求覆盖：全面覆盖 Require.md 1-15 项，彻底剔除文件级轮询依赖。
"""
import asyncio
import json
import sys
from datetime import date, datetime, timedelta

from agent.dingtalk_client import DingTalkClient
from agent.llm_client import ReportGenerator
from common.config_loader import Config
from common.logger import get_logger, setup_logging
from common.user_store import UserStore
from mcp_server.services.dingtalk_api import DingTalkService
from mcp_server.services.local_fs import LocalFileService

setup_logging()
logger = get_logger("Agent_Main")

_dingtalk = DingTalkClient()
_last_report_date: dict[str, date] = {}


def _check_preconditions(user_id: str) -> bool:
    is_holiday, reason = LocalFileService.is_holiday()
    if is_holiday: return False
    is_on_leave, leave_reason = DingTalkService.is_user_on_leave(user_id=user_id)
    if is_on_leave: return False
    return True


def _build_report_for_user(user_id: str) -> tuple[dict, int]:
    """严格对齐当日工作并清理过期"""
    UserStore.clean_outdated(user_id)
    tasks = UserStore.get_tasks(user_id)
    version = UserStore.get_task_version(user_id)

    today_str = datetime.now().strftime("%Y-%m-%d")

    # 严格按照当天切分
    today_t = [t for t in tasks if t["date"] == today_str]
    future_t = [t for t in tasks if t["date"] > today_str]

    if not today_t and not future_t:
        return {"today_work": "（今日无任务）", "tomorrow_plan": "（无）", "summary_card": ""}, version

    report = ReportGenerator().generate(today_t, future_t)
    return report, version


async def _call_mcp_send(report: dict, user_id: str) -> tuple[bool, str]:
    logger.info(f"→ 通过子进程唤起 MCP Server 为用户 {user_id} 发送日报...")
    template_id = UserStore.get_template_id(user_id)
    # 核心修改：动态获取该模板的字段配置
    contents_config = UserStore.get_template_contents(user_id, template_id)

    payload_str = json.dumps({
        "today_work": report.get("today_work", ""),
        "tomorrow_plan": report.get("tomorrow_plan", ""),
        "user_id": user_id,
        "template_id": template_id,
        "contents_config": contents_config,
    }, ensure_ascii=False)

    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "mcp_server.server",
            "--action", "send_report",
            "--payload", payload_str,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        output = stdout.decode("utf-8", errors="replace").strip()

        if proc.returncode == 0:
            logger.info(f"✅ MCP 发送成功: {output}")
            report_id = ""
            try:
                report_id = json.loads(output).get("report_id", "")
            except Exception:
                pass
            return True, report_id
        else:
            err_msg = stderr.decode("utf-8", errors="replace").strip()
            logger.error(f"❌ MCP 子进程返回非零: {err_msg}")
            return False, err_msg
    except asyncio.TimeoutError:
        return False, "发送超时（>30s）"
    except Exception as e:
        return False, str(e)


async def _wait_for_confirm_or_timeout(
        user_id: str, timeout_min: int, initial_version: int,
) -> tuple[str, dict | None]:
    """完全基于内存中 task_version 变化的热更新等待循环"""
    deadline = datetime.now() + timedelta(minutes=timeout_min)
    check_interval = Config.get("scheduler.check_interval_sec", 10)
    current_version = initial_version

    logger.info(f"⏳ 用户 {user_id} 进入双模等待，{timeout_min} 分钟（至 {deadline.strftime('%H:%M:%S')}）")

    while datetime.now() < deadline:
        remaining = (deadline - datetime.now()).total_seconds()

        # 检查 Y/N 回复
        response = UserStore.get_response_nowait(user_id)
        if response == "Y":
            return "confirmed", None
        elif response == "N":
            return "cancelled", None

        # 检查基于 WebSocket 的任务实时更新版本
        new_version = UserStore.get_task_version(user_id)
        if new_version != current_version:
            logger.info(f"🔄 用户 {user_id} 任务更新（version {current_version}→{new_version}），重新生成日报...")
            new_report, _ = _build_report_for_user(user_id)
            current_version = new_version
            return "regenerated", new_report

        await asyncio.sleep(min(check_interval, remaining))

    logger.info(f"⌛ 用户 {user_id} 等待超时，触发自动发送")
    return "timeout", None


async def execute_report_workflow(user_id: str):
    logger.info(f"🚀 开始执行用户 {user_id} 的日报工作流")

    if not _check_preconditions(user_id):
        logger.info(f"⏭️  用户 {user_id} 前置检查未通过，跳过日报生成")
        return

    today = datetime.now().date()
    if _last_report_date.get(user_id) == today:
        logger.info(f"⚠️  用户 {user_id} 今日已发送日报，跳过")
        return

    # 核心修复：先清理过期任务，再获取有效任务
    logger.info(f"🗑️ 清理用户 {user_id} 的过期任务...")
    UserStore.clean_outdated(user_id)

    tasks = UserStore.get_tasks(user_id)
    if not tasks:
        logger.info(f"⚠️  用户 {user_id} 无有效任务数据（可能已全部过期），等待用户在钉钉发送任务清单")
        return

    logger.info(f"📋 用户 {user_id} 当前有 {len(tasks)} 条有效任务")

    timeout_min = Config.get("scheduler.confirm_timeout_min", 15)
    report, version = _build_report_for_user(user_id)

    logger.info(f"✅ LLM 日报生成完成")
    logger.debug(f"今日工作: {report.get('today_work', '')[:100]}")
    logger.debug(f"明日计划: {report.get('tomorrow_plan', '')[:100]}")

    iteration = 0
    outcome = "timeout"

    while True:
        iteration += 1
        if iteration > 10:
            logger.warning("⚠️  热更新循环超过上限，强制发送")
            break

        title = f"工作日报预览（{datetime.now().strftime('%m/%d %H:%M')}）"
        logger.info(f"📤 发送预览卡片 (第 {iteration} 次)")

        sent_ok = _dingtalk.send_card_to_user(
            title=title, today_work=report.get("today_work", "（无）"),
            tomorrow_plan=report.get("tomorrow_plan", "（无）"),
            countdown_min=timeout_min, mode="auto", user_id=user_id,
        )

        if not sent_ok:
            logger.error("❌ 发送预览卡片失败，终止工作流")
            return

        logger.info(f"✅ 预览卡片发送成功，进入等待确认阶段")

        outcome, new_report = await _wait_for_confirm_or_timeout(user_id, timeout_min, version)

        if outcome == "regenerated":
            logger.info("🔄 检测到任务更新，重新生成日报")
            if new_report is not None:
                report = new_report
            version = UserStore.get_task_version(user_id)
            continue
        break

    if outcome == "cancelled":
        logger.info("❌ 用户取消日报发送")
        _dingtalk.send_text_to_user("已取消本次日报发送，今日不再自动提交。", user_id=user_id)
        return

    logger.info(f"📮 开始提交日报到钉钉日志系统")
    success, detail = await _call_mcp_send(report, user_id)

    logger.info(f"📨 发送结果通知")
    _dingtalk.send_result_card_to_user(success=success, report_id=detail if success else "",
                                       error=detail if not success else "", user_id=user_id)

    if success:
        _last_report_date[user_id] = today
        logger.info(f"🎉 用户 {user_id} 日报发送成功，报告ID: {detail}")
    else:
        logger.error(f"❌ 用户 {user_id} 日报发送失败: {detail}")


async def main():
    logger.info("=" * 60)
    logger.info("  LingXi Daily Agent 启动")
    logger.info("=" * 60)

    if not _dingtalk.is_configured:
        logger.error("❌ 钉钉配置不完整，请检查 .env 文件")
        return

    # 自动检查并更新节假日数据（完全自动化，无需手动维护）
    logger.info("📅 检查节假日数据...")
    try:
        from common.holiday_auto_update import check_and_update_holidays
        check_and_update_holidays()
    except Exception as e:
        logger.warning(f"⚠️  节假日数据检查失败，将使用降级逻辑: {e}")

    report_time_str = Config.get("scheduler.report_time", "18:30")
    report_hour, report_minute = map(int, report_time_str.split(":"))

    _dingtalk.start_message_listener()

    for uid in UserStore.all_user_ids():
        UserStore.get_or_create(uid)

    configured_users = UserStore.all_user_ids()
    if "--test" in sys.argv:
        idx = sys.argv.index("--test")
        test_user = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else (
            configured_users[0] if configured_users else Config.USER_ID)
        await execute_report_workflow(test_user)
        return

    # 使用精确的时间调度，避免轮询竞态条件
    from datetime import timedelta
    
    logger.info(f"⏰ 等待每日 {report_time_str} 触发日报...")
    
    # 记录已触发的用户和日期，防止重复发送
    triggered_reports: set[str] = set()

    while True:
        now = datetime.now()
        today = now.date()
        
        # 计算今天的触发时间点
        today_trigger = now.replace(hour=report_hour, minute=report_minute, second=0, microsecond=0)
        
        # 如果当前时间已过今天的触发时间，则计算明天的触发时间
        if now >= today_trigger:
            next_trigger = today_trigger + timedelta(days=1)
        else:
            next_trigger = today_trigger
        
        # 清理过期的触发记录（只保留今天的）
        triggered_reports = {k for k in triggered_reports if k.endswith(str(today))}
        
        # 等待到下一个触发时间点
        wait_seconds = (next_trigger - now).total_seconds()
        if wait_seconds > 0:
            logger.debug(f"⏳ 下次触发时间: {next_trigger.strftime('%Y-%m-%d %H:%M:%S')}, 等待 {wait_seconds:.0f} 秒")
            await asyncio.sleep(wait_seconds)
        
        # 触发时刻到达，执行日报工作流
        trigger_date = next_trigger.date()
        all_users = UserStore.all_user_ids() or [Config.USER_ID]
        
        for uid in all_users:
            day_key = f"{uid}:{trigger_date}"
            if day_key not in triggered_reports:
                triggered_reports.add(day_key)
                logger.info(f"🚀 触发用户 {uid} 的日报工作流 (日期: {trigger_date})")
                asyncio.create_task(execute_report_workflow(uid))
            else:
                logger.debug(f"⚠️  用户 {uid} 今日已触发，跳过")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Agent 已停止")
    except Exception as e:
        logger.critical(f"致命错误: {e}", exc_info=True)
