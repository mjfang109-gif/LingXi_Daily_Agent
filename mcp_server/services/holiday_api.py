import datetime
import traceback

import requests

from common.logger import get_logger

logger = get_logger("Holiday_Service")


class HolidayService:
    @classmethod
    def get_status(cls, date_str: str = None) -> dict:
        """
        调用公共 API 查询指定日期的节假日状态
        API 返回的 type 枚举: 0: 工作日, 1: 周末, 2: 节假日, 3: 调休工作日
        """
        # 如果不传日期，默认查今天
        if not date_str:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")

        logger.info(f"--- [API Call] 开始查询法定节假日, 日期: {date_str} ---")

        # 使用 Timor 免费节假日 API
        url = f"https://timor.tech/api/holiday/info/{date_str}"

        # 伪装一下请求头，防止被免费 API 拦截
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)
            res_json = response.json()

            if res_json.get("code") == 0:
                type_info = res_json.get("type", {})
                day_type = type_info.get("type")
                name = type_info.get("name", "普通")

                logger.info(f"✅ 查询成功: {date_str} 的状态类型为 {day_type} ({name})")

                if day_type == 0:
                    return {"success": True, "is_workday": True, "desc": "普通工作日"}
                elif day_type == 1:
                    return {"success": True, "is_workday": False, "desc": "普通周末"}
                elif day_type == 2:
                    return {"success": True, "is_workday": False, "desc": f"法定节假日 ({name})"}
                elif day_type == 3:
                    return {"success": True, "is_workday": True, "desc": f"调休工作日 ({name})"}
            else:
                logger.error(f"❌ 节假日 API 返回错误: {res_json}")
                return {"success": False, "error": "API 状态码异常"}

        except requests.exceptions.Timeout:
            logger.error("❌ 查询节假日 API 超时")
            return cls._fallback_calculation(date_str, "网络超时")
        except Exception as e:
            logger.error(f"❌ 查询节假日发生异常: {e}")
            logger.debug(traceback.format_exc())
            return cls._fallback_calculation(date_str, str(e))

    @classmethod
    def _fallback_calculation(cls, date_str: str, reason: str) -> dict:
        """
        兜底降级逻辑：如果外部 API 挂了，我们不能让 Agent 崩溃。
        直接用 Python 内置库计算今天是周几，做基础的周末判断。
        """
        logger.warning(f"⚠️ 触发节假日降级判断逻辑，原因: {reason}")
        try:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            is_weekend = dt.weekday() >= 5  # 5 是周六，6 是周日

            if is_weekend:
                return {"success": True, "is_workday": False, "desc": "周末(降级判断)"}
            else:
                return {"success": True, "is_workday": True, "desc": "工作日(降级判断)"}
        except Exception:
            # 最极端的兜底：默认要写日报
            return {"success": True, "is_workday": True, "desc": "未知(异常兜底为工作日)"}
