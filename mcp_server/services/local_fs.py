"""
LocalFileService — 读取本地 holiday.json 做节假日判断（需求 4）
JSON 格式示例：
{
  "2025-01-01": "元旦(休)",
  "2025-02-08": "春节调休(班)"
}
"""
import json
import os
from datetime import datetime

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("LocalFS_Service")


class LocalFileService:
    @staticmethod
    def is_holiday(date_str: str | None = None) -> tuple[bool, str]:
        """
        返回 (是否阻断, 原因说明)
        """
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        holiday_file = Config.get("paths.holiday_file", "./holiday.json")

        if not os.path.exists(holiday_file):
            logger.warning(f"节假日文件不存在: {holiday_file}，默认放行")
            return False, "未配置节假日文件"

        try:
            with open(holiday_file, "r", encoding="utf-8") as f:
                data: dict = json.load(f)

            status = data.get(date_str, "")
            if "(休)" in status:
                return True, f"法定节假日: {status}"
            if "(班)" in status:
                return False, f"调休工作日: {status}"

            # 未记录 → 按周末判断
            is_weekend = datetime.strptime(date_str, "%Y-%m-%d").weekday() >= 5
            if is_weekend:
                return True, "普通周末"
            return False, "普通工作日"

        except Exception as e:
            logger.error(f"读取节假日文件异常: {e}")
            return False, f"读取异常: {e}"
