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
    logger.info(f"Agent 请求检查环境门控，user_id={user_id or '默认'}")

    is_holiday, holiday_reason = LocalFileService.is_holiday()
    if is_holiday:
        return {"can_run": False, "reason": holiday_reason}

    is_on_leave, leave_reason = DingTalkService.is_user_on_leave(
        user_id=user_id or None
    )
    if is_on_leave:
        return {"can_run": False, "reason": leave_reason}

    return {"can_run": True, "reason": "工作日且正常在岗"}


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
    logger.info(f"Agent 请求发送钉钉日报，user_id={user_id or '默认'}")
    try:
        cfg = json.loads(contents_config) if contents_config and contents_config != "[]" else None
        res = DingTalkService.create_report(
            today_work, tomorrow_plan,
            user_id=user_id or None,
            template_id=template_id or None,
            contents_config=cfg,
        )
        if res.get("success"):
            return json.dumps(
                {"success": True, "report_id": res.get("report_id", "")},
                ensure_ascii=False,
            )
        return json.dumps({"success": False, "error": "未知错误"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"路由层异常: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@mcp.tool()
def check_statutory_holiday(date_str: str = "") -> str:
    """查询指定日期是否为法定节假日（需求 4/5），date_str: YYYY-MM-DD，不传查今天"""
    logger.info(f"节假日查询: {date_str or '今天'}")
    is_off, reason = LocalFileService.is_holiday(date_str or None)
    if is_off:
        return f"🛑 休息日。{reason}。建议中止日报流程。"
    return f"✅ 工作日。{reason}。请继续执行日报工作流。"


@mcp.tool()
def get_dingtalk_userid(mobile: str) -> str:
    """【初始化工具】根据手机号查询钉钉 UserID"""
    res = DingTalkService.get_userid_by_mobile(mobile)
    if res.get("success"):
        return (
            f"✅ UserID: {res['userid']}\n"
            f"💡 请写入 .env 的 DINGTALK_USER_ID 或 config.yaml 的 users 列表"
        )
    return f"❌ 查询失败: {res.get('error')}"


@mcp.tool()
def get_dingtalk_templates(user_id: str) -> str:
    """【初始化工具】查询用户可见的日志模板列表"""
    res = DingTalkService.get_report_templates(user_id)
    if not res.get("success"):
        return f"❌ 获取模板失败: {res.get('error')}"
    templates = res.get("templates", [])
    if not templates:
        return "⚠️ 该用户没有可见的日志模板"
    lines = [f"📋 共 {len(templates)} 个模板:"]
    for t in templates:
        lines.append(f"  - 【{t['name']}】 ID: {t['template_id']}")
    lines.append("\n💡 将目标模板 ID 写入 .env 的 DINGTALK_TEMPLATE_ID 或 config.yaml users[].template_id")
    return "\n".join(lines)


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
    logger.info(f"Agent 请求发送钉钉卡片，user_id={user_id or '默认'}")
    try:
        success = DingTalkMessageService.send_card_to_user(
            title, today_work, tomorrow_plan, summary_card,
            countdown_min, mode, user_id=user_id or None,
        )
        return json.dumps({"success": success}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"发送卡片异常: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@mcp.tool()
def send_dingtalk_text(content: str, user_id: str = "") -> str:
    """发送钉钉文本消息给用户"""
    logger.info(f"Agent 请求发送钉钉文本，user_id={user_id or '默认'}")
    try:
        success = DingTalkMessageService.send_text_to_user(content, user_id=user_id or None)
        return json.dumps({"success": success}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"发送文本异常: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@mcp.tool()
def send_dingtalk_result(
        success: bool,
        report_id: str = "",
        error: str = "",
        user_id: str = "",
) -> str:
    """发送钉钉结果通知卡片"""
    try:
        result = DingTalkMessageService.send_result_card_to_user(
            success, report_id, error, user_id=user_id or None,
        )
        return json.dumps({"success": result}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"发送结果卡片异常: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════
#  CLI 子进程模式（需求 12）
# ═══════════════════════════════════════════════════════════════

def _cli_main():
    parser = argparse.ArgumentParser(description="MCP Server CLI 模式")
    parser.add_argument("--action", required=True, help="要执行的动作")
    parser.add_argument("--payload", default="{}", help="JSON 格式的参数")
    args = parser.parse_args()

    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError as e:
        print(json.dumps({"success": False, "error": f"Payload JSON 解析失败: {e}"}))
        sys.exit(1)

    if args.action == "send_report":
        today_work = payload.get("today_work", "")
        tomorrow_plan = payload.get("tomorrow_plan", "")

        if not today_work and not tomorrow_plan:
            print(json.dumps({"success": False, "error": "today_work 和 tomorrow_plan 均为空"}))
            sys.exit(1)

        user_id = payload.get("user_id") or None
        template_id = payload.get("template_id") or None
        contents_config = payload.get("contents_config") or None

        try:
            res = DingTalkService.create_report(
                today_work, tomorrow_plan,
                user_id=user_id,
                template_id=template_id,
                contents_config=contents_config,
            )
            if res.get("success"):
                print(json.dumps(
                    {"success": True, "report_id": res.get("report_id", "")},
                    ensure_ascii=False,
                ))
                sys.exit(0)
            else:
                print(json.dumps({"success": False, "error": "未知错误"}, ensure_ascii=False))
                sys.exit(1)
        except Exception as e:
            print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
            sys.exit(1)

    elif args.action == "check_env":
        user_id = payload.get("user_id") or None
        is_holiday, reason = LocalFileService.is_holiday()
        if is_holiday:
            print(json.dumps({"can_run": False, "reason": reason}, ensure_ascii=False))
        else:
            is_leave, reason2 = DingTalkService.is_user_on_leave(user_id=user_id)
            if is_leave:
                print(json.dumps({"can_run": False, "reason": reason2}, ensure_ascii=False))
            else:
                print(json.dumps({"can_run": True, "reason": "工作日且正常在岗"}, ensure_ascii=False))
        sys.exit(0)

    else:
        print(json.dumps({"success": False, "error": f"未知 action: {args.action}"}))
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