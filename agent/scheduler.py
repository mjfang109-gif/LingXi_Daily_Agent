"""
Scheduler — 轻量定时包装器（保留兼容接口）
主要调度逻辑已内联到 agent/main.py asyncio 主循环中。
此模块保留供外部脚本按需调用。
"""
import asyncio

import schedule
import time

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("Scheduler")


def start_daily_job(async_job_func):
    """
    将异步工作流函数挂载到 schedule，用同步 wrapper 包裹后执行。
    report_time 从 config.yaml 读取。
    """
    report_time = Config.get("scheduler.report_time", "17:50")

    def _run():
        asyncio.run(async_job_func())

    schedule.every().day.at(report_time).do(_run)
    logger.info(f"📅 定时任务已注册，每日 {report_time} 执行")

    while True:
        schedule.run_pending()
        time.sleep(10)
