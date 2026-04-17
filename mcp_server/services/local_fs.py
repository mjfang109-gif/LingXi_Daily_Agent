"""
LocalFileService — 读取本地 holiday.json 判断节假日（需求 4/5）

JSON 格式（与实际 holiday.json 对齐，只读，不修改）：
{
  "2026-01-01": { "date": "2026-01-01", "name": "元旦", "isOffDay": true },
  "2026-01-04": { "date": "2026-01-04", "name": "元旦调休", "isOffDay": false }
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
        读取本地 holiday.json，判断指定日期是否为休息日。
        返回 (是否阻断, 原因说明)。

        优先级：
          1. JSON 中有记录 → 按 isOffDay 字段判断
          2. JSON 无记录   → 按 Python weekday() 判断周末
          3. 文件不存在    → 默认放行（不阻断）
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

            day_info = data.get(date_str)

            if day_info is None:
                # JSON 未记录此日期 → 降级为 Python 内置周末判断
                is_weekend = datetime.strptime(date_str, "%Y-%m-%d").weekday() >= 5
                if is_weekend:
                    return True, "普通周末"
                return False, "普通工作日"

            # 按 isOffDay 字段判断（需求 5）
            is_off = day_info.get("isOffDay", False)
            name = day_info.get("name", "")

            if is_off:
                return True, f"法定节假日: {name}"
            else:
                return False, f"调休工作日: {name}"

        except json.JSONDecodeError as e:
            logger.error(f"解析节假日文件失败（JSON 格式错误）: {e}")
            return False, f"文件格式错误: {e}"
        except Exception as e:
            logger.error(f"读取节假日文件异常: {e}")
            return False, f"读取异常: {e}"
