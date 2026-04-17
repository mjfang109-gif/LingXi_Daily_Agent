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
        
        Args:
            date_str (str | None): 日期字符串，格式为 YYYY-MM-DD。如果为 None，则使用当前日期。
            
        Returns:
            dict: 包含查询结果的字典。
                - success (bool): 是否查询成功。
                - is_workday (bool): 是否为工作日。
                - desc (str): 日期描述。
                - error (str, optional): 错误信息（仅在 success 为 False 时存在）。
                
        API type 枚举: 
            0: 工作日
            1: 周末
            2: 节假日
            3: 调休工作日
        """
        # 处理默认日期参数
        if not date_str:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            
        logger.info(f"[HolidayService.get_status] 开始查询节假日状态 | 入参: date_str={date_str}")

        url = _API_URL.format(date=date_str)
        logger.debug(f"[HolidayService.get_status] 构造请求 URL: {url} | Headers: {_HEADERS}")

        try:
            # 发起 HTTP GET 请求
            logger.info(f"[HolidayService.get_status] 发起 API 请求 | URL: {url} | Timeout: 5s")
            resp = requests.get(url, headers=_HEADERS, timeout=5)
            
            # 记录响应状态码和原始内容片段（避免日志过长）
            logger.debug(f"[HolidayService.get_status] API 响应状态码: {resp.status_code} | 响应内容前200字符: {resp.text[:200]}")
            
            data = resp.json()
            logger.debug(f"[HolidayService.get_status] API 响应解析后的 JSON 数据: {data}")

            # 检查 API 业务状态码
            if data.get("code") != 0:
                logger.error(f"[HolidayService.get_status] API 返回业务错误 | 入参: date_str={date_str} | 响应数据: {data}")
                return {"success": False, "error": "API 状态码异常"}

            # 提取关键字段
            t = data.get("type", {})
            day_type = t.get("type")
            name = t.get("name", "普通")
            
            logger.info(f"[HolidayService.get_status] API 查询成功 | 入参: date_str={date_str} | 出参: type={day_type}, name={name}")

            # 定义类型映射关系
            _MAP = {
                0: {"is_workday": True, "desc": "普通工作日"},
                1: {"is_workday": False, "desc": "普通周末"},
                2: {"is_workday": False, "desc": f"法定节假日 ({name})"},
                3: {"is_workday": True, "desc": f"调休工作日 ({name})"},
            }
            
            # 获取对应的描述信息，默认为未知
            info = _MAP.get(day_type, {"is_workday": True, "desc": "未知类型"})
            
            result = {"success": True, **info}
            logger.info(f"[HolidayService.get_status] 最终返回结果 | 入参: date_str={date_str} | 出参: {result}")
            return result

        except requests.exceptions.Timeout:
            error_msg = "网络超时"
            logger.error(f"[HolidayService.get_status] 请求超时 | 入参: date_str={date_str} | 错误: {error_msg}")
            return cls._fallback(date_str, error_msg)
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[HolidayService.get_status] 发生未预期异常 | 入参: date_str={date_str} | 错误类型: {type(e).__name__} | 错误信息: {error_msg}")
            logger.debug(f"[HolidayService.get_status] 异常堆栈跟踪:\n{traceback.format_exc()}")
            return cls._fallback(date_str, error_msg)

    @classmethod
    def _fallback(cls, date_str: str, reason: str) -> dict:
        """
        API 不可用时降级为 Python 内置周末判断逻辑。
        
        Args:
            date_str (str): 日期字符串，格式为 YYYY-MM-DD。
            reason (str): 触发降级的原因。
            
        Returns:
            dict: 降级后的查询结果。
                - success (bool): 固定为 True。
                - is_workday (bool): 根据本地时间计算是否为工作日。
                - desc (str): 描述信息，标注为降级结果。
        """
        logger.warning(f"[HolidayService._fallback] 触发降级逻辑 | 入参: date_str={date_str}, reason={reason}")
        
        try:
            # 解析日期字符串
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            # weekday(): 0=Monday, 6=Sunday. >=5 表示周六或周日
            is_weekend = dt.weekday() >= 5
            is_workday = not is_weekend
            
            desc = "周末(降级)" if is_weekend else "工作日(降级)"
            
            result = {
                "success": True,
                "is_workday": is_workday,
                "desc": desc,
            }
            
            logger.info(f"[HolidayService._fallback] 降级计算完成 | 入参: date_str={date_str} | 出参: is_workday={is_workday}, desc={desc}")
            return result
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[HolidayService._fallback] 降级逻辑执行异常 | 入参: date_str={date_str}, reason={reason} | 异常: {error_msg}")
            logger.debug(f"[HolidayService._fallback] 降级异常堆栈:\n{traceback.format_exc()}")
            
            # 极端异常情况下的兜底返回
            fallback_result = {"success": True, "is_workday": True, "desc": "未知(异常兜底为工作日)"}
            logger.warning(f"[HolidayService._fallback] 返回极端兜底结果 | 出参: {fallback_result}")
            return fallback_result
