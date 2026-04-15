import os
import sys

from mcp.server.fastmcp import FastMCP

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import get_logger
from mcp_server.services.dingtalk_api import DingTalkService
from mcp_server.services.local_fs import LocalFileService
from mcp_server.services.holiday_api import HolidayService

logger = get_logger("MCP_Router")
mcp = FastMCP("DingTalkTools")


@mcp.tool()
def check_environment_status() -> dict:
    """
    环境门控核心 Tool。Agent 在生成日报前必须调用此工具。
    返回是否允许发送日报的综合判定。
    """
    logger.info("Agent 请求检查环境门控状态...")

    # 1. 检查节假日
    is_holiday, holiday_reason = LocalFileService.is_holiday()
    if is_holiday:
        logger.info(f"环境门控阻断: {holiday_reason}")
        return {"can_run": False, "reason": holiday_reason}

    # 2. 检查钉钉请假状态
    is_on_leave, leave_reason = DingTalkService.is_user_on_leave()
    if is_on_leave:
        logger.info(f"环境门控阻断: {leave_reason}")
        return {"can_run": False, "reason": leave_reason}

    logger.info("环境门控检查通过，允许生成日报。")
    return {"can_run": True, "reason": "工作日且正常在岗"}


@mcp.tool()
def send_dingtalk_report(today_work: str, tomorrow_plan: str) -> str:
    """发送工作日报到钉钉"""
    logger.info("Agent 请求发送钉钉日报")
    try:
        res = DingTalkService.create_report(today_work, tomorrow_plan)
        if res.get("errcode") == 0:
            return f"✅ 发送成功，日志ID: {res.get('result', {}).get('report_id')}"
        else:
            return f"❌ 发送失败: {res.get('errmsg')}"
    except Exception as e:
        logger.error(f"路由层捕获异常: {e}")
        return f"❌ 系统异常: {e}"


@mcp.tool()
def get_dingtalk_userid(mobile: str) -> str:
    """
    【初始化工具 1】根据手机号查询钉钉 UserID。
    如果缺少 DINGTALK_USER_ID，请先调用此工具。
    """
    logger.info(f"MCP 接收到 UserID 查询请求，手机号: {mobile}")

    user_res = DingTalkService.get_userid_by_mobile(mobile)
    if not user_res.get("success"):
        return f"❌ 查询 UserID 失败:\n{user_res.get('error')}"

    user_id = user_res.get("userid")
    return f"✅ 成功获取 UserID: {user_id}\n💡 请将此 ID 配置到环境变量 DINGTALK_USER_ID 中。"


@mcp.tool()
def get_dingtalk_templates(user_id: str) -> str:
    """
    【初始化工具 2】根据 UserID 查询该用户可见的所有日志模板列表。
    必须先获取到 UserID 后，才能调用此工具查询模板。
    """
    logger.info(f"MCP 接收到模板查询请求，UserID: {user_id}")

    tpl_res = DingTalkService.get_report_templates(user_id)
    if not tpl_res.get("success"):
        return f"❌ 获取日志模板失败: {tpl_res.get('error')}"

    templates = tpl_res.get("templates", [])
    if not templates:
        return "⚠️ 查询成功，但该用户当前没有任何可见的日志模板。"

    output = [f"📋 该用户可见的日志模板 ({len(templates)}个):"]
    for t in templates:
        output.append(f"  - 模板名称: 【{t['name']}】 | ID: {t['template_id']}")

    output.append("\n💡 请挑选您要发送的模板，将其 ID 配置到环境变量 DINGTALK_TEMPLATE_ID 中。")
    return "\n".join(output)


@mcp.tool()
def check_statutory_holiday(date_str: str = None) -> str:
    """
    【日程工具】查询指定日期是否为法定节假日、调休工作日或普通周末。
    参数 date_str: 日期字符串，格式为 YYYY-MM-DD。如果不传，则默认查询今天。
    用途: 在生成日报或安排任务前，判断当天是否需要工作。
    """
    logger.info(f"MCP 接收到节假日查询请求，目标日期: {date_str if date_str else '今天'}")

    result = HolidayService.get_status(date_str)

    if not result.get("success"):
        return f"查询失败: {result.get('error')}。系统已触发降级逻辑，建议按普通工作日/周末规则处理。"

    is_work = result.get("is_workday")
    desc = result.get("desc")

    # 返回给 Agent 的自然语言描述越清晰越好
    if is_work:
        return f"✅ 需要工作。该日期为：{desc}。请继续执行生成日报等工作流。"
    else:
        return f"🛑 休息日。该日期为：{desc}。如果是今天，建议中止发日报的流程并提示用户正在休息。"


if __name__ == "__main__":
    logger.info("MCP Server 已启动，加载门控服务与钉钉服务完成。")
    mcp.run()
