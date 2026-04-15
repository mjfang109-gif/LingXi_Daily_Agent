import asyncio
import hashlib
import json
from datetime import datetime, timedelta

from agent.llm_client import ReportGenerator
from agent.parser import TodoParser
from agent.dingtalk_client import DingTalkClient
from common.config_loader import Config
from common.logger import setup_logging, get_logger

setup_logging()
logger = get_logger("Agent_Main")

# 初始化钉钉客户端 (全局唯一实例)
dingtalk_client = DingTalkClient()

# 用于跟踪上次日报生成日期，确保每天只生成一次
last_report_date = None


def get_file_md5(path):
    """计算文件的MD5值"""
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except FileNotFoundError:
        logger.error(f"文件未找到: {path}")
        return ""
    except Exception as e:
        logger.error(f"计算文件MD5时出错: {e}")
        return ""


def get_dingtalk_attendance_status():
    """
    模拟获取钉钉考勤状态，增加容错处理。
    如果接口调用失败，默认返回 "normal"。
    """
    try:
        logger.info("正在查询钉钉考勤状态...")
        # 模拟实际的API调用，这里可能抛出异常或返回不同状态
        # 例如：response = requests.get("https://api.dingtalk.com/v1.0/attendance/...")
        # if response.status_code == 200 and response.json().get('result') == 'leave':
        #     return "leave"
        return "normal"  # 默认返回正常
    except Exception as e:
        logger.warning(f"查询钉钉考勤状态失败: {e}。将按默认状态（正常）继续执行。")
        return "normal"


def check_preconditions():
    """
    检查是否满足执行条件：非节假日、非请假状态
    """
    # 1. 节假日检查
    holiday_path = Config.get("paths.holiday_file")
    today_str = datetime.now().strftime("%Y-%m-%d")
    year_str = datetime.now().strftime("%Y")
    try:
        with open(holiday_path, 'r', encoding='utf-8') as f:
            holidays = json.load(f)
        
        all_holiday_dates = []
        if year_str in holidays:
            for holiday_dates in holidays[year_str].values():
                all_holiday_dates.extend(holiday_dates)

        if today_str in all_holiday_dates:
            logger.info(f"今天是节假日 ({today_str})，任务自动跳过。")
            return False
    except FileNotFoundError:
        logger.warning(f"节假日文件 {holiday_path} 未找到，跳过检查。")
    except Exception as e:
        logger.error(f"检查节假日时出错: {e}")

    # 2. 考勤状态检查
    attendance_status = get_dingtalk_attendance_status()
    if attendance_status == "leave":
        logger.info("检测到用户处于“请假”状态，日报任务自动静默退出。")
        return False
    
    logger.info("前置条件检查通过，准备生成日报。")
    return True


async def call_mcp_send(report):
    """
    调用MCP发送日报，并根据结果发送不同的钉钉通知。
    """
    try:
        logger.info("正在调用 MCP Client 发送日报...")
        # 模拟实际的MCP发送逻辑，这里可能抛出异常
        # success = mcp_client.send(report)
        # if not success:
        #    raise Exception("MCP client returned False")
        await asyncio.sleep(1) # 模拟IO操作
        
        logger.info("日报发送成功！")
        await dingtalk_client.send_text_to_user("✅ 您的工作日报已成功发送。")
        return True
    except Exception as e:
        logger.error(f"调用 MCP 发送日报失败: {e}")
        error_message = (
            f"🔥 **日报自动发送失败** 🔥\\n\\n"
            f"原因: `{e}`\\n\\n"
            f"请您手动复制下方的日报内容进行发送。"
        )
        await dingtalk_client.send_markdown_to_user("日报发送失败提醒", error_message)
        return False


async def execute_report_workflow():
    """
    执行日报生成、预览和发送的完整工作流。
    """
    global last_report_date

    if not check_preconditions():
        return

    todo_path = Config.get("paths.todo_file")
    
    logger.info("开始生成日报...")
    tasks = TodoParser.parse_file(todo_path)
    report = ReportGenerator().generate(tasks)

    # 格式化预览内容
    title = "✨ 工作日报预览"
    today_work = report.get('today_work', '无').replace('\\n', '\n\n')
    tomorrow_plan = report.get('tomorrow_plan', '无').replace('\\n', '\n\n')
    summary_card = report.get('summary_card', '无')

    markdown_text = f"### {title}\n\n"
    markdown_text += f"#### 今日工作\n\n{today_work}\n\n"
    markdown_text += f"#### 明日计划\n\n{tomorrow_plan}\n\n"
    markdown_text += f"#### 任务摘要\n\n{summary_card}\n\n"
    markdown_text += f"> 此为自动生成日报预览，无需确认，将直接发送。"

    # 发送预览到钉钉
    dingtalk_client.send_markdown_to_user(title, markdown_text)
    logger.info("日报预览已发送至钉钉。")

    # 直接发送日报 (不再等待确认)
    if await call_mcp_send(report):
        last_report_date = datetime.now().date() # 记录成功发送的日期
    
    logger.info("日报工作流执行完毕。")


async def main_agent_loop():
    """
    Agent的主循环，负责定时触发日报工作流。
    """
    logger.info("=" * 60)
    logger.info("LingXi Daily Agent 启动")
    logger.info("=" * 60)

    # 检查钉钉配置是否完整
    if not dingtalk_client.is_configured:
        logger.error("❌ 钉钉客户端配置不完整，请检查 .env 文件中的 DINGTALK_CLIENT_ID, DINGTALK_CLIENT_SECRET, DINGTALK_ROBOT_CODE, DINGTALK_CHAT_ID, DINGTALK_USER_ID。")
        return

    report_time_str = Config.get("scheduler.report_time", "17:50")
    try:
        report_hour, report_minute = map(int, report_time_str.split(':'))
    except ValueError:
        logger.error(f"❌ 配置中日报时间格式错误: {report_time_str}。请使用 HH:MM 格式。")
        # 默认一个时间，防止程序崩溃
        report_hour, report_minute = 17, 50

    logger.info(f"📅 日报生成任务将在每天 {report_time_str} 触发。")

    global last_report_date

    while True:
        now = datetime.now()
        today = now.date()

        # 检查是否到了触发时间，并且今天还没有生成过日报
        if now.hour == report_hour and now.minute == report_minute and today != last_report_date:
            logger.info(f"⏰ 达到日报生成时间 ({report_time_str})，触发工作流...")
            await execute_report_workflow()
            # 成功触发后，更新日期，避免在同一分钟内重复触发
            last_report_date = today
            # 触发后等待一分钟，避免在同一分钟内重复执行
            await asyncio.sleep(60) 
        else:
            # 每隔一段时间检查一次时间
            await asyncio.sleep(10)

if __name__ == '__main__':
    try:
        asyncio.run(main_agent_loop())
    except KeyboardInterrupt:
        logger.info("Agent 已通过 Ctrl+C 停止。")
    except Exception as e:
        logger.critical(f"Agent 运行过程中发生未捕获的致命错误: {e}", exc_info=True)
