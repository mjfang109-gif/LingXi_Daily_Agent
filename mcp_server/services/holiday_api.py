"""
HolidayService — 节假日状态查询（在线 API + 降级兜底）
"""
import datetime
import traceback

import requests

from common.logger import get_logger

logger = get_logger("Holiday_Service")

_API_URL = "https://timor.tech/api/holiday/info/{date}"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


class HolidayService:
    @classmethod
    def get_status(cls, date_str: str | None = None) -> dict:
        """
        查询指定日期的节假日状态。
        API type 枚举: 0 工作日, 1 周末, 2 节假日, 3 调休工作日
        """
        if not date_str:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")

        logger.info(f"--- [API Call] 节假日查询: {date_str} ---")
        url = _API_URL.format(date=date_str)

        try:
            resp = requests.get(url, headers=_HEADERS, timeout=5)
            data = resp.json()

            if data.get("code") != 0:
                logger.error(f"节假日 API 异常响应: {data}")
                return {"success": False, "error": "API 状态码异常"}

            t = data.get("type", {})
            day_type = t.get("type")
            name = t.get("name", "普通")
            logger.info(f"✅ 节假日查询成功: {date_str} = type {day_type} ({name})")

            _MAP = {
                0: {"is_workday": True,  "desc": "普通工作日"},
                1: {"is_workday": False, "desc": "普通周末"},
                2: {"is_workday": False, "desc": f"法定节假日 ({name})"},
                3: {"is_workday": True,  "desc": f"调休工作日 ({name})"},
            }
            info = _MAP.get(day_type, {"is_workday": True, "desc": "未知"})
            return {"success": True, **info}

        except requests.exceptions.Timeout:
            logger.error("节假日 API 超时")
            return cls._fallback(date_str, "网络超时")
        except Exception as e:
            logger.error(f"节假日查询异常: {e}")
            logger.debug(traceback.format_exc())
            return cls._fallback(date_str, str(e))

    @classmethod
    def _fallback(cls, date_str: str, reason: str) -> dict:
        """API 不可用时降级为 Python 内置周末判断"""
        logger.warning(f"⚠️  节假日降级判断，原因: {reason}")
        try:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            is_weekend = dt.weekday() >= 5
            return {
                "success":    True,
                "is_workday": not is_weekend,
                "desc":       "周末(降级)" if is_weekend else "工作日(降级)",
            }
        except Exception:
            return {"success": True, "is_workday": True, "desc": "未知(异常兜底为工作日)"}
