"""
MCP Server — 钉钉工具路由层（需求 11/12）

两种启动方式：
  1. FastMCP 模式（Agent 通过 MCP 协议调用）：
       python -m mcp_server.server
  2. CLI 子进程模式（Agent 通过 subprocess 解耦调用）：
       python -m mcp_server.server --action send_report --payload '{"today_work":"...","tomorrow_plan":"..."}'
"""
import argparse
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP

from common.logger import get_logger, setup_logging
from mcp_server.services.dingtalk_api import DingTalkService
from mcp_server.services.holiday_api import HolidayService
from mcp_server.services.local_fs import LocalFileService

setup_logging()
logger = get_logger("MCP_Server")
mcp = FastMCP("LingXiDailyTools")


# ═══════════════════════════════════════════════════════════════
#  MCP Tools（FastMCP 协议模式）
# ═══════════════════════════════════════════════════════════════

@mcp.tool()
def check_environment_status() -> dict:
    """
    环境门控核心 Tool（需求 3/4/5）
    Agent 在生成日报前必须调用此工具，返回综合放行判定。
    """
    logger.info("Agent 请求检查环境门控...")

    is_holiday, holiday_reason = LocalFileService.is_holiday()
    if is_holiday:
        logger.info(f"门控阻断: {holiday_reason}")
        return {"can_run": False, "reason": holiday_reason}

    is_on_leave, leave_reason = DingTalkService.is_user_on_leave()
    if is_on_leave:
        logger.info(f"门控阻断: {leave_reason}")
        return {"can_run": False, "reason": leave_reason}

    logger.info("✅ 环境门控通过")
    return {"can_run": True, "reason": "工作日且正常在岗"}


@mcp.tool()
def send_dingtalk_report(today_work: str, tomorrow_plan: str) -> str:
    """
    发送工作日报到钉钉日志（需求 12）
    Agent 调用此工具，底层走 DingTalkService.create_report
    """
    logger.info("Agent 请求发送钉钉日报")
    try:
        res = DingTalkService.create_report(today_work, tomorrow_plan)

        # create_report 返回的格式是 {"success": bool, "report_id": str, "data": ...}
        if res.get("success"):
            report_id = res.get("report_id", "")
            return json.dumps({"success": True, "report_id": report_id}, ensure_ascii=False)
        else:
            return json.dumps({"success": False, "error": "未知错误"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"路由层异常: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@mcp.tool()
def check_statutory_holiday(date_str: str = None) -> str:
    """
    查询指定日期是否为法定节假日（需求 4）
    date_str: YYYY-MM-DD，不传则查今天
    """
    logger.info(f"节假日查询: {date_str or '今天'}")
    result = HolidayService.get_status(date_str)

    if not result.get("success"):
        return f"查询失败: {result.get('error')}。建议按工作日处理。"

    is_work = result["is_workday"]
    desc = result["desc"]
    if is_work:
        return f"✅ 需要工作。该日期为：{desc}。请继续执行日报工作流。"
    return f"🛑 休息日。该日期为：{desc}。建议中止日报流程。"


@mcp.tool()
def get_dingtalk_userid(mobile: str) -> str:
    """【初始化工具】根据手机号查询钉钉 UserID"""
    res = DingTalkService.get_userid_by_mobile(mobile)
    if res.get("success"):
        return f"✅ UserID: {res['userid']}\n💡 请写入 .env 的 DINGTALK_USER_ID"
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
    lines.append("\n💡 将目标模板 ID 写入 .env 的 DINGTALK_TEMPLATE_ID")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  CLI 子进程模式（需求 12：Agent 通过 subprocess 极致解耦调用）
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

        try:
            res = DingTalkService.create_report(today_work, tomorrow_plan)

            # create_report 返回的格式是 {"success": bool, "report_id": str, "data": ...}
            if res.get("success"):
                report_id = res.get("report_id", "")
                print(json.dumps({"success": True, "report_id": report_id}, ensure_ascii=False))
                sys.exit(0)
            else:
                print(json.dumps({"success": False, "error": "未知错误"}, ensure_ascii=False))
                sys.exit(1)
        except Exception as e:
            print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
            sys.exit(1)

    elif args.action == "check_env":
        is_holiday, reason = LocalFileService.is_holiday()
        if is_holiday:
            print(json.dumps({"can_run": False, "reason": reason}, ensure_ascii=False))
        else:
            is_leave, reason2 = DingTalkService.is_user_on_leave()
            if is_leave:
                print(json.dumps({"can_run": False, "reason": reason2}, ensure_ascii=False))
            else:
                print(json.dumps({"can_run": True, "reason": "工作日且正常在岗"}, ensure_ascii=False))
        sys.exit(0)

    else:
        print(json.dumps({"success": False, "error": f"未知 action: {args.action}"}))
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════
#  入口判断
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if "--action" in sys.argv:
        # CLI 子进程模式
        _cli_main()
    else:
        # FastMCP 服务模式
        logger.info("MCP Server 启动（FastMCP 协议模式）")
        mcp.run()
