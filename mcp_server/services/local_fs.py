import os
import json
from datetime import datetime
from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("LocalFS_Service")


class LocalFileService:
    @staticmethod
    def is_holiday(date_str: str = None) -> tuple[bool, str]:
        """
        检查指定日期是否为法定节假日
        返回: (是否阻断发送, 原因说明)
        """
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        holiday_file = Config.get("paths.holiday_file")
        if not os.path.exists(holiday_file):
            logger.warning(f"缺失节假日配置文件: {holiday_file}，默认放行。")
            return False, "未配置日历"

        try:
            with open(holiday_file, 'r', encoding='utf-8') as f:
                holidays_data = json.load(f)

            status = holidays_data.get(date_str)
            if status and "(休)" in status:
                return True, f"法定节假日: {status}"
            elif status and "(班)" in status:
                return False, f"调休工作日: {status}"
            else:
                # 若日历中没有这一天，可以通过 Python 内置的 weekday 简单判断周末
                # 0-4 为周一到周五，5-6 为周末
                is_weekend = datetime.strptime(date_str, "%Y-%m-%d").weekday() >= 5
                if is_weekend:
                    return True, "普通周末"
                return False, "普通工作日"

        except Exception as e:
            logger.error(f"读取节假日文件异常: {e}")
            return False, "读取异常"