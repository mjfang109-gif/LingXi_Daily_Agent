"""
MCP Server — 钉钉工具路由层（需求 11/12）

两种启动方式：
  1. FastMCP 模式（Claude Desktop/MCP 协议调用）：
       python -m mcp_server.server
  2. CLI 子进程模式（Agent 通过 subprocess 解耦调用）：
       python -m mcp_server.server --action send_report --payload '{"today_work":"...","tomorrow_plan":"...","user_id":"xxx","template_id":"yyy"}'
"""
import argparse
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP

from common.logger import get_logger, setup_logging
from mcp_server.services.dingtalk_api import DingTalkService
from mcp_server.services.dingtalk_message import DingTalkMessageService
from mcp_server.services.local_fs import LocalFileService

setup_logging()
logger = get_logger("MCP_Server")
mcp = FastMCP("LingXiDailyTools")


# ═══════════════════════════════════════════════════════════════
#  MCP Tools（FastMCP 协议模式）
# ═══════════════════════════════════════════════════════════════

@mcp.tool()
def check_environment_status(user_id: str = "") -> dict:
    """
    环境门控（需求 4/5/6）
    检查节假日（本地 JSON）+ 用户考勤状态，返回综合放行判定。
    """
    logger.info(f"[check_environment_status] 收到请求 | 入参: user_id={user_id or '默认'}")

    # 1. 检查是否为节假日
    is_holiday, holiday_reason = LocalFileService.is_holiday()
    logger.info(f"[check_environment_status] 节假日检查结果 | is_holiday={is_holiday}, reason={holiday_reason}")
    if is_holiday:
        res = {"can_run": False, "reason": holiday_reason}
        logger.info(f"[check_environment_status] 拦截原因: 节假日 | 出参: {res}")
        return res

    # 2. 检查用户考勤状态
    effective_user_id = user_id or None
    is_on_leave, leave_reason = DingTalkService.is_user_on_leave(user_id=effective_user_id)
    logger.info(
        f"[check_environment_status] 考勤检查结果 | user_id={effective_user_id}, is_on_leave={is_on_leave}, reason={leave_reason}")
    if is_on_leave:
        res = {"can_run": False, "reason": leave_reason}
        logger.info(f"[check_environment_status] 拦截原因: 请假/缺勤 | 出参: {res}")
        return res

    res = {"can_run": True, "reason": "工作日且正常在岗"}
    logger.info(f"[check_environment_status] 检查通过 | 出参: {res}")
    return res


@mcp.tool()
def send_dingtalk_report(
        today_work: str,
        tomorrow_plan: str,
        user_id: str = "",
        template_id: str = "",
        contents_config: str = "[]",
) -> str:
    """
    发送工作日报到钉钉日志（需求 12/14/15）
    contents_config: JSON 字符串，格式 [{"sort":1,"key":"今日工作"},{"sort":2,"key":"明日计划"}]
    """
    logger.info(
        f"[send_dingtalk_report] 收到请求 | 入参: "
        f"user_id={user_id or '默认'}, "
        f"template_id={template_id or '默认'}, "
        f"today_work_len={len(today_work)}, "
        f"tomorrow_plan_len={len(tomorrow_plan)}, "
        f"contents_config={contents_config}"
    )
    try:
        # 解析配置
        cfg = None
        if contents_config and contents_config != "[]":
            try:
                cfg = json.loads(contents_config)
                logger.info(f"[send_dingtalk_report] contents_config 解析成功: {cfg}")
            except json.JSONDecodeError as e:
                logger.error(f"[send_dingtalk_report] contents_config 解析失败: {e}")
                return json.dumps({"success": False, "error": f"contents_config 格式错误: {str(e)}"},
                                  ensure_ascii=False)

        effective_user_id = user_id or None
        effective_template_id = template_id or None

        # 调用底层服务
        logger.info(
            f"[send_dingtalk_report] 调用 DingTalkService.create_report | "
            f"user_id={effective_user_id}, template_id={effective_template_id}"
        )
        res = DingTalkService.create_report(
            today_work, tomorrow_plan,
            user_id=effective_user_id,
            template_id=effective_template_id,
            contents_config=cfg,
        )
        logger.info(f"[send_dingtalk_report] DingTalkService 返回结果: {res}")

        if res.get("success"):
            out_res = {
                "success": True,
                "report_id": res.get("report_id", "")
            }
            logger.info(f"[send_dingtalk_report] 发送成功 | 出参: {out_res}")
            return json.dumps(out_res, ensure_ascii=False)

        error_msg = res.get("error", "未知错误")
        out_res = {"success": False, "error": error_msg}
        logger.warning(f"[send_dingtalk_report] 发送失败 | 出参: {out_res}")
        return json.dumps(out_res, ensure_ascii=False)

    except Exception as e:
        logger.error(f"[send_dingtalk_report] 路由层异常: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@mcp.tool()
def check_statutory_holiday(date_str: str = "") -> str:
    """查询指定日期是否为法定节假日（需求 4/5），date_str: YYYY-MM-DD，不传查今天"""
    logger.info(f"[check_statutory_holiday] 收到请求 | 入参: date_str={date_str or '今天'}")

    target_date = date_str or None
    is_off, reason = LocalFileService.is_holiday(target_date)
    logger.info(f"[check_statutory_holiday] 查询结果 | date={target_date}, is_off={is_off}, reason={reason}")

    if is_off:
        msg = f"🛑 休息日。{reason}。建议中止日报流程。"
        logger.info(f"[check_statutory_holiday] 出参: {msg}")
        return msg

    msg = f"✅ 工作日。{reason}。请继续执行日报工作流。"
    logger.info(f"[check_statutory_holiday] 出参: {msg}")
    return msg


@mcp.tool()
def get_dingtalk_userid(mobile: str) -> str:
    """【初始化工具】根据手机号查询钉钉 UserID"""
    logger.info(f"[get_dingtalk_userid] 收到请求 | 入参: mobile={mobile}")

    res = DingTalkService.get_userid_by_mobile(mobile)
    logger.info(f"[get_dingtalk_userid] 服务返回: {res}")

    if res.get("success"):
        userid = res['userid']
        msg = (
            f"✅ UserID: {userid}\n"
            f"💡 请写入 .env 的 DINGTALK_USER_ID 或 config.yaml 的 users 列表"
        )
        logger.info(f"[get_dingtalk_userid] 查询成功 | 出参: UserID={userid}")
        return msg

    error_msg = res.get('error', '未知错误')
    msg = f"❌ 查询失败: {error_msg}"
    logger.warning(f"[get_dingtalk_userid] 查询失败 | 出参: {msg}")
    return msg


@mcp.tool()
def get_dingtalk_templates(user_id: str) -> str:
    """【初始化工具】查询用户可见的日志模板列表"""
    logger.info(f"[get_dingtalk_templates] 收到请求 | 入参: user_id={user_id}")

    res = DingTalkService.get_report_templates(user_id)
    logger.info(f"[get_dingtalk_templates] 服务返回 success={res.get('success')}")

    if not res.get("success"):
        error_msg = res.get('error', '未知错误')
        msg = f"❌ 获取模板失败: {error_msg}"
        logger.warning(f"[get_dingtalk_templates] 获取失败 | 出参: {msg}")
        return msg

    templates = res.get("templates", [])
    logger.info(f"[get_dingtalk_templates] 获取到模板数量: {len(templates)}")

    if not templates:
        msg = "⚠️ 该用户没有可见的日志模板"
        logger.info(f"[get_dingtalk_templates] 模板为空 | 出参: {msg}")
        return msg

    lines = [f"📋 共 {len(templates)} 个模板:"]
    for t in templates:
        lines.append(f"  - 【{t['name']}】 ID: {t['template_id']}")
    lines.append("\n💡 将目标模板 ID 写入 .env 的 DINGTALK_TEMPLATE_ID 或 config.yaml users[].template_id")

    result_str = "\n".join(lines)
    logger.info(f"[get_dingtalk_templates] 构建完成 | 出参长度: {len(result_str)}")
    return result_str


@mcp.tool()
def send_dingtalk_card(
        title: str,
        today_work: str,
        tomorrow_plan: str,
        summary_card: str = "",
        countdown_min: int = 15,
        mode: str = "auto",
        user_id: str = "",
) -> str:
    """发送钉钉卡片消息给用户（用于日报预览）"""
    logger.info(
        f"[send_dingtalk_card] 收到请求 | 入参: "
        f"user_id={user_id or '默认'}, title={title}, "
        f"countdown_min={countdown_min}, mode={mode}"
    )
    try:
        effective_user_id = user_id or None
        logger.info(
            f"[send_dingtalk_card] 调用 DingTalkMessageService.send_card_to_user | "
            f"user_id={effective_user_id}"
        )
        success = DingTalkMessageService.send_card_to_user(
            title, today_work, tomorrow_plan,
            countdown_min, mode, user_id=effective_user_id,
        )
        logger.info(f"[send_dingtalk_card] 发送结果: success={success}")

        out_res = {"success": success}
        logger.info(f"[send_dingtalk_card] 出参: {out_res}")
        return json.dumps(out_res, ensure_ascii=False)
    except Exception as e:
        logger.error(f"[send_dingtalk_card] 发送卡片异常: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@mcp.tool()
def send_dingtalk_text(content: str, user_id: str = "") -> str:
    """发送钉钉文本消息给用户"""
    logger.info(
        f"[send_dingtalk_text] 收到请求 | 入参: "
        f"user_id={user_id or '默认'}, content_len={len(content)}"
    )
    try:
        effective_user_id = user_id or None
        logger.info(
            f"[send_dingtalk_text] 调用 DingTalkMessageService.send_text_to_user | "
            f"user_id={effective_user_id}"
        )
        success = DingTalkMessageService.send_text_to_user(content, user_id=effective_user_id)
        logger.info(f"[send_dingtalk_text] 发送结果: success={success}")

        out_res = {"success": success}
        logger.info(f"[send_dingtalk_text] 出参: {out_res}")
        return json.dumps(out_res, ensure_ascii=False)
    except Exception as e:
        logger.error(f"[send_dingtalk_text] 发送文本异常: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@mcp.tool()
def send_dingtalk_result(
        success: bool,
        report_id: str = "",
        error: str = "",
        user_id: str = "",
) -> str:
    """发送钉钉结果通知卡片"""
    logger.info(
        f"[send_dingtalk_result] 收到请求 | 入参: "
        f"user_id={user_id or '默认'}, success={success}, "
        f"report_id={report_id}, error={error}"
    )
    try:
        effective_user_id = user_id or None
        logger.info(
            f"[send_dingtalk_result] 调用 DingTalkMessageService.send_result_card_to_user | "
            f"user_id={effective_user_id}"
        )
        result = DingTalkMessageService.send_result_card_to_user(
            success, report_id, error, user_id=effective_user_id,
        )
        logger.info(f"[send_dingtalk_result] 发送结果: {result}")

        out_res = {"success": result}
        logger.info(f"[send_dingtalk_result] 出参: {out_res}")
        return json.dumps(out_res, ensure_ascii=False)
    except Exception as e:
        logger.error(f"[send_dingtalk_result] 发送结果卡片异常: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════
#  CLI 子进程模式（需求 12）
# ═══════════════════════════════════════════════════════════════

def _cli_main():
    parser = argparse.ArgumentParser(description="MCP Server CLI 模式")
    parser.add_argument("--action", required=True, help="要执行的动作")
    parser.add_argument("--payload", default="{}", help="JSON 格式的参数")
    args = parser.parse_args()

    logger.info(f"[CLI] 启动 CLI 模式 | action={args.action}")

    try:
        payload = json.loads(args.payload)
        logger.info(f"[CLI] Payload 解析成功: {payload}")
    except json.JSONDecodeError as e:
        error_msg = f"Payload JSON 解析失败: {e}"
        logger.error(f"[CLI] {error_msg}")
        print(json.dumps({"success": False, "error": error_msg}))
        sys.exit(1)

    if args.action == "send_report":
        logger.info("[CLI] 执行动作: send_report")
        today_work = payload.get("today_work", "")
        tomorrow_plan = payload.get("tomorrow_plan", "")

        if not today_work and not tomorrow_plan:
            error_msg = "today_work 和 tomorrow_plan 均为空"
            logger.warning(f"[CLI] {error_msg}")
            print(json.dumps({"success": False, "error": error_msg}))
            sys.exit(1)

        user_id = payload.get("user_id") or None
        template_id = payload.get("template_id") or None
        contents_config = payload.get("contents_config") or None

        logger.info(
            f"[CLI] send_report 参数 | user_id={user_id}, template_id={template_id}, "
            f"today_work_len={len(today_work)}, tomorrow_plan_len={len(tomorrow_plan)}"
        )

        try:
            logger.info("[CLI] 调用 DingTalkService.create_report")
            res = DingTalkService.create_report(
                today_work, tomorrow_plan,
                user_id=user_id,
                template_id=template_id,
                contents_config=contents_config,
            )
            logger.info(f"[CLI] create_report 返回: {res}")

            if res.get("success"):
                out_res = {
                    "success": True,
                    "report_id": res.get("report_id", "")
                }
                logger.info(f"[CLI] send_report 成功 | 输出: {out_res}")
                print(json.dumps(out_res, ensure_ascii=False))
                sys.exit(0)
            else:
                error_msg = res.get("error", "未知错误")
                out_res = {"success": False, "error": error_msg}
                logger.warning(f"[CLI] send_report 失败 | 输出: {out_res}")
                print(json.dumps(out_res, ensure_ascii=False))
                sys.exit(1)
        except Exception as e:
            logger.error(f"[CLI] send_report 异常: {e}", exc_info=True)
            print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
            sys.exit(1)

    elif args.action == "check_env":
        logger.info("[CLI] 执行动作: check_env")
        user_id = payload.get("user_id") or None
        logger.info(f"[CLI] check_env 参数 | user_id={user_id}")

        is_holiday, reason = LocalFileService.is_holiday()
        logger.info(f"[CLI] 节假日检查 | is_holiday={is_holiday}, reason={reason}")

        if is_holiday:
            out_res = {"can_run": False, "reason": reason}
            logger.info(f"[CLI] check_env 结果: 节假日拦截 | 输出: {out_res}")
            print(json.dumps(out_res, ensure_ascii=False))
        else:
            is_leave, reason2 = DingTalkService.is_user_on_leave(user_id=user_id)
            logger.info(f"[CLI] 考勤检查 | is_leave={is_leave}, reason={reason2}")
            if is_leave:
                out_res = {"can_run": False, "reason": reason2}
                logger.info(f"[CLI] check_env 结果: 考勤拦截 | 输出: {out_res}")
                print(json.dumps(out_res, ensure_ascii=False))
            else:
                out_res = {"can_run": True, "reason": "工作日且正常在岗"}
                logger.info(f"[CLI] check_env 结果: 通过 | 输出: {out_res}")
                print(json.dumps(out_res, ensure_ascii=False))
        sys.exit(0)

    else:
        error_msg = f"未知 action: {args.action}"
        logger.error(f"[CLI] {error_msg}")
        print(json.dumps({"success": False, "error": error_msg}))
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════
#  入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if "--action" in sys.argv:
        _cli_main()
    else:
        logger.info("MCP Server 启动（FastMCP 协议模式）")
        mcp.run()
