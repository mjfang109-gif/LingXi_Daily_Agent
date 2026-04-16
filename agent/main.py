"""
LingXi Daily Agent — 主工作流编排（需求 7/10）

工作流：
  1. 前置门控检查（节假日 + 请假状态）
  2. 解析 todo.md → LLM 润色 → 计算 MD5
  3. 通过钉钉机器人单聊用户发送「普通卡片」预览
  4. 进入 15 分钟双模等待：
       • 手动模式：用户在钉钉回复 Y → 立即发送
       • 热更新：todo.md 变动 → 重新生成并重置倒计时（需求 10）
       • 超时自动：15 分钟无响应 → 自动调用 MCP 发送
  5. 通过 MCP 子进程调用钉钉日报 API 发送（需求 11/12）
"""
import asyncio
import hashlib
import json
import os
import subprocess
import sys
from datetime import date, datetime, timedelta
from typing import Optional

from agent.dingtalk_client import DingTalkClient
from agent.llm_client import ReportGenerator
from agent.parser import TodoParser
from common.config_loader import Config
from common.logger import get_logger, setup_logging

setup_logging()
logger = get_logger("Agent_Main")

# ── 全局单例 ──────────────────────────────────────────────────
_dingtalk = DingTalkClient()
_last_report_date: Optional[date] = None  # 防止当日重复触发


# ═══════════════════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════════════════

def _md5_file(path: str) -> str:
    """计算文件 MD5，文件不存在返回空串"""
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except FileNotFoundError:
        return ""
    except Exception as e:
        logger.error(f"计算 MD5 异常: {e}")
        return ""


def _check_holiday() -> tuple[bool, str]:
    """
    节假日门控（需求 4）
    读取 holiday.json，根据 isOffDay 字段判断是否为休息日
    """
    holiday_file = Config.get("paths.holiday_file", "./holiday.json")
    today = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(holiday_file):
        logger.warning(f"节假日文件不存在: {holiday_file}，默认放行")
        return False, "未配置节假日文件"

    try:
        with open(holiday_file, "r", encoding="utf-8") as f:
            data: dict = json.load(f)

        day_info = data.get(today)

        # JSON 无记录时，降级为 Python 内置周末判断
        if day_info is None:
            if datetime.strptime(today, "%Y-%m-%d").weekday() >= 5:
                return True, "普通周末"
            return False, "普通工作日"

        # 根据 isOffDay 字段判断
        is_off_day = day_info.get("isOffDay", False)
        holiday_name = day_info.get("name", "")

        if is_off_day:
            return True, f"法定节假日: {holiday_name}"
        else:
            return False, f"调休工作日: {holiday_name}"

    except Exception as e:
        logger.error(f"读取节假日文件失败: {e}")
        return False, "读取异常（默认放行）"


def _check_attendance() -> tuple[bool, str]:
    """
    钉钉考勤状态门控（需求 5）
    使用钉钉考勤接口：POST /topapi/attendance/getusergroup
    或使用审批接口：POST /topapi/processinstance/listids
    """
    try:
        if not Config.USER_ID:
            logger.warning("未配置 USER_ID，跳过考勤查询")
            return False, "未配置用户ID"

        from mcp_server.services.dingtalk_api import DingTalkService
        return DingTalkService.is_user_on_leave()

    except Exception as e:
        logger.warning(f"考勤接口异常: {e}，默认放行")
        return False, f"考勤接口异常: {e}"


def _check_preconditions() -> bool:
    """整合环境门控（需求 3/4/5）"""
    is_holiday, reason = _check_holiday()
    if is_holiday:
        logger.info(f"🛑 环境门控阻断 — {reason}")
        return False

    is_on_leave, reason = _check_attendance()
    if is_on_leave:
        logger.info(f"🛑 环境门控阻断 — {reason}")
        return False

    logger.info("✅ 前置门控通过，准备生成日报")
    return True


def _build_report(todo_path: str) -> tuple[dict, str]:
    """
    解析 todo.md → LLM 润色，返回 (report_dict, file_md5)
    """
    tasks = TodoParser.parse_file(todo_path)
    report = ReportGenerator().generate(tasks)
    md5 = _md5_file(todo_path)
    return report, md5


# ═══════════════════════════════════════════════════════════════
#  MCP 解耦调用（需求 11/12）
# ═══════════════════════════════════════════════════════════════

async def _call_mcp_send(report: dict) -> tuple[bool, str]:
    """
    通过独立子进程唤起 mcp_server，极致解耦（需求 12）
    Agent 作为"大脑"不碰底层 API（需求 11）
    """
    logger.info("→ 通过子进程唤起 MCP Server 发送日报...")
    payload_str = json.dumps(
        {
            "today_work": report.get("today_work", ""),
            "tomorrow_plan": report.get("tomorrow_plan", ""),
        },
        ensure_ascii=False,
    )

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
            # 尝试从输出中解析 report_id
            report_id = ""
            try:
                out_json = json.loads(output)
                report_id = out_json.get("report_id", "")
            except Exception:
                pass
            return True, report_id
        else:
            err_msg = stderr.decode("utf-8", errors="replace").strip()
            logger.error(f"❌ MCP 子进程返回非零: {err_msg}")
            return False, err_msg

    except asyncio.TimeoutError:
        logger.error("❌ MCP 子进程超时")
        return False, "发送超时（>30s）"
    except Exception as e:
        logger.error(f"❌ 唤起 MCP 子进程异常: {e}")
        return False, str(e)


# ═══════════════════════════════════════════════════════════════
#  双模确认 + 热更新等待（需求 7/10）
# ═══════════════════════════════════════════════════════════════

async def _wait_for_confirm_or_timeout(
        timeout_min: int,
        todo_path: str,
        initial_md5: str,
) -> tuple[str, dict | None]:
    """
    等待期间：
      - 每 check_interval_sec 秒检测 todo.md 是否变动（需求 10）
      - 用户在钉钉回复 Y → 返回 ("confirmed", None)
      - 用户在钉钉回复 N → 返回 ("cancelled", None)
      - 文件变动    → 重新生成报告，返回 ("regenerated", new_report)
      - 超时        → 返回 ("timeout", None)
    """
    deadline = datetime.now() + timedelta(minutes=timeout_min)
    check_interval = Config.get("scheduler.check_interval_sec", 10)
    current_md5 = initial_md5

    logger.info(f"⏳ 进入双模等待，超时时间 {timeout_min} 分钟（{deadline.strftime('%H:%M:%S')} 前）")

    while datetime.now() < deadline:
        remaining = (deadline - datetime.now()).total_seconds()

        # ① 检查用户钉钉回复
        user_input = await DingTalkClient.get_user_response(timeout=0)
        if user_input == "Y":
            logger.info("👤 用户钉钉回复 Y，立即发送")
            return "confirmed", None
        elif user_input == "N":
            logger.info("👤 用户钉钉回复 N，取消发送")
            return "cancelled", None

        # ② 热更新检测（需求 10）
        new_md5 = _md5_file(todo_path)
        if new_md5 and new_md5 != current_md5:
            logger.info("🔄 检测到 todo.md 内容变更，重新生成日报并重置倒计时...")
            new_report, new_md5 = _build_report(todo_path)
            current_md5 = new_md5
            return "regenerated", new_report

        await asyncio.sleep(min(check_interval, remaining))

    logger.info("⌛ 等待超时，触发自动发送")
    return "timeout", None


# ═══════════════════════════════════════════════════════════════
#  完整工作流
# ═══════════════════════════════════════════════════════════════

async def execute_report_workflow():
    """执行一次完整的日报工作流"""
    global _last_report_date

    # 门控检查
    if not _check_preconditions():
        return

    todo_path = Config.get("paths.todo_file", "./todo.md")
    timeout_min = Config.get("scheduler.confirm_timeout_min", 15)
    report, md5 = _build_report(todo_path)

    logger.info("📋 日报已生成，准备发送预览卡片...")

    # 循环处理热更新：发卡片 → 等待 → 若触发热更新则重发卡片
    iteration = 0
    while True:
        iteration += 1
        if iteration > 10:  # 防御性上限
            logger.warning("⚠️  热更新循环次数超过上限，强制发送")
            break

        # 发送预览卡片（需求 7）
        title = f"✨ 工作日报预览（{datetime.now().strftime('%m/%d %H:%M')}）"
        sent_ok = _dingtalk.send_card_to_user(
            title=title,
            today_work=report.get("today_work", "（无）"),
            tomorrow_plan=report.get("tomorrow_plan", "（无）"),
            summary_card=report.get("summary_card", ""),
            countdown_min=timeout_min,
            mode="auto",
        )
        if not sent_ok:
            logger.error("❌ 卡片发送失败，中止工作流")
            return

        # 进入双模等待
        outcome, new_report = await _wait_for_confirm_or_timeout(timeout_min, todo_path, md5)

        if outcome == "regenerated":
            # 文件变动 → 用新报告重新循环
            report = new_report
            md5 = _md5_file(todo_path)
            logger.info("🔄 用更新后的内容重新发送预览卡片...")
            continue

        # 确认 / 超时 / 取消 → 跳出循环
        break

    if outcome == "cancelled":
        _dingtalk.send_text_to_user("ℹ️  已取消本次日报发送，今日不再自动提交。")
        logger.info("用户取消，工作流结束")
        return

    # 通过 MCP 发送日报（需求 11/12）
    logger.info("📤 开始通过 MCP 发送日报...")
    success, detail = await _call_mcp_send(report)

    # 发送结果通知卡片
    _dingtalk.send_result_card_to_user(
        success=success,
        report_id=detail if success else "",
        error=detail if not success else "",
    )

    if success:
        _last_report_date = datetime.now().date()
        logger.info("🎉 日报发送成功，工作流完成")
    else:
        logger.error(f"💥 日报发送失败: {detail}")


# ═══════════════════════════════════════════════════════════════
#  主循环
# ═══════════════════════════════════════════════════════════════
async def main():
    global _last_report_date

    logger.info("=" * 60)
    logger.info("  LingXi Daily Agent 启动")
    logger.info("=" * 60)

    if not _dingtalk.is_configured:
        logger.error("❌ 钉钉配置不完整，请检查 .env 文件（CLIENT_ID/SECRET/ROBOT_CODE/USER_ID）")
        return

    report_time_str = Config.get("scheduler.report_time", "17:50")
    try:
        report_hour, report_minute = map(int, report_time_str.split(":"))
    except ValueError:
        logger.error(f"日报时间格式错误: {report_time_str}，默认使用 17:50")
        report_hour, report_minute = 17, 50

    logger.info(f"📅 每日 {report_time_str} 触发日报生成")
    logger.info("💬 等待触发... (在钉钉回复 Y 确认 / N 取消)")

    # 启动钉钉消息监听
    callback_port = Config.get("server.callback_port", 8080)
    _dingtalk.start_message_listener(port=callback_port)
    logger.info(f"📡 钉钉消息监听已启动，端口: {callback_port}")

    # 测试模式：立即执行一次工作流
    test_mode = "--test" in sys.argv
    if test_mode:
        logger.info("🧪 测试模式：立即执行日报工作流...")
        await execute_report_workflow()
        logger.info("🧪 测试完成，退出程序")
        return

    while True:
        now = datetime.now()
        if (
                now.hour == report_hour
                and now.minute == report_minute
                and now.date() != _last_report_date
        ):
            logger.info(f"⏰ 触发时间 {report_time_str} 到达，启动工作流...")
            await execute_report_workflow()
            _last_report_date = now.date()
            await asyncio.sleep(60)  # 防止同分钟重复触发
        else:
            await asyncio.sleep(10)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Agent 已停止")
    except Exception as e:
        logger.critical(f"致命错误: {e}", exc_info=True)
