import sys
import os
from mcp.server.fastmcp import FastMCP

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import get_logger
from mcp_server.services.dingtalk_api import DingTalkService
from mcp_server.services.local_fs import LocalFileService

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


if __name__ == "__main__":
    logger.info("MCP Server 已启动，加载门控服务与钉钉服务完成。")
    mcp.run()
