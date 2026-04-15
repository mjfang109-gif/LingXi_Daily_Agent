import time

import schedule

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("Scheduler")


def start_daily_job(job_func):
    """启动基于配置的定时任务"""
    report_time = Config.get("scheduler.report_time", "17:50")

    # 每天固定时间执行
    schedule.every().day.at(report_time).do(job_func)

    logger.info(f"📅 定时任务已启动，每日执行时间: {report_time}")

    while True:
        schedule.run_pending()
        time.sleep(10)  # 每10秒检查一次任务队列
