"""
DingTalkService — 钉钉底层 API 封装（MCP 层使用）
职责：Token 缓存、日志提交、用户 ID 查询、模板查询
使用 requests 直接调用钉钉 API
"""
import json
import time
import traceback

import requests

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("DingTalk_Service")


class DingTalkService:
    _token: str | None = None
    _token_expire_at: float = 0

    @staticmethod
    def _mask(secret: str) -> str:
        if not secret or len(secret) < 6:
            return "***"
        return f"{secret[:3]}***{secret[-3:]}"

    # ── Token ─────────────────────────────────────────────────

    @classmethod
    def get_token(cls) -> str:
        """获取 AccessToken，本地缓存 115 分钟"""
        if cls._token and time.time() < cls._token_expire_at:
            return cls._token

        if not Config.CLIENT_ID or not Config.CLIENT_SECRET:
            raise ValueError("缺少 DINGTALK_CLIENT_ID / CLIENT_SECRET")

        url = "https://oapi.dingtalk.com/gettoken"
        params = {
            "appkey": Config.CLIENT_ID,
            "appsecret": Config.CLIENT_SECRET
        }

        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()

            if data.get("errcode") != 0:
                raise RuntimeError(f"Token 获取失败: {data.get('errmsg')}")

            cls._token = data["access_token"]
            cls._token_expire_at = time.time() + 6900  # 7200s - 5min 缓冲
            logger.info("✅ DingTalk AccessToken 已刷新")
            return cls._token

        except Exception as e:
            logger.error(f"获取 Token 失败: {e}")
            raise

    # ── 发送日志 ──────────────────────────────────────────────

    @classmethod
    def create_report(cls, today_work: str, tomorrow_plan: str) -> dict:
        """
        提交钉钉工作日志
        接口：POST /topapi/report/create
        文档：https://open.dingtalk.com/document/isvapp/enterprise-creates-a-log
        """
        logger.info("--- [API Call] 提交钉钉工作日志 ---")
        try:
            token = cls.get_token()
            template_id = Config.TEMPLATE_ID
            user_id = Config.USER_ID

            if not template_id:
                raise RuntimeError("未配置 DINGTALK_TEMPLATE_ID，请在 .env 文件中添加")

            if not user_id:
                raise RuntimeError("未配置 DINGTALK_USER_ID，请在 .env 文件中添加")

            logger.info(f"使用模板 ID: {template_id}, 用户 ID: {user_id}")

            # 从配置获取字段名称（可选，默认使用以下值）
            today_key = Config.get("dingtalk.report_field_today", "今日工作")
            tomorrow_key = Config.get("dingtalk.report_field_tomorrow", "明日计划")
            dd_from = Config.get("dingtalk.report_dd_from", "report")

            # 构造日志内容 - 按照钉钉 API 要求的格式
            contents = [
                {
                    "content_type": "markdown",
                    "sort": 1,
                    "type": 1,
                    "content": today_work,
                    "key": today_key
                },
                {
                    "content_type": "markdown",
                    "sort": 2,
                    "type": 1,
                    "content": tomorrow_plan,
                    "key": tomorrow_key
                }
            ]

            # 构造请求参数 - 完全按照 curl 的格式
            url = f"https://oapi.dingtalk.com/topapi/report/create?access_token={token}"

            create_report_param = {
                "contents": contents,
                "template_id": template_id,
                "to_chat": False,
                "dd_from": dd_from,
                "userid": user_id
            }

            payload = {
                "create_report_param": create_report_param
            }

            headers = {"Content-Type": "application/json"}
            logger.debug(f"Payload: {json.dumps(payload, ensure_ascii=False)}")

            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            result = resp.json()

            # 检查响应
            if result.get("errcode") != 0:
                error_msg = result.get("errmsg", "未知错误")
                raise RuntimeError(f"提交日志失败 (errcode={result.get('errcode')}): {error_msg}")

            report_id = result.get("result", "")
            logger.info(f"✅ 日志提交成功，报告 ID: {report_id}")
            logger.debug(f"钉钉响应: {json.dumps(result, ensure_ascii=False)}")

            return {
                "success": True,
                "report_id": report_id,
                "data": result
            }

        except Exception as e:
            logger.error(f"❌ 提交日志异常: {e}")
            logger.debug(traceback.format_exc())
            raise

    # ── 考勤状态 ──────────────────────────────────────────────

    @classmethod
    def is_user_on_leave(cls) -> tuple[bool, str]:
        """
        查询当前用户是否处于请假状态（需求 5）
        使用钉钉考勤接口：POST /topapi/attendance/getusergroup
        """
        try:
            if not Config.USER_ID:
                logger.warning("未配置 USER_ID，跳过考勤查询")
                return False, "未配置用户ID"

            token = cls.get_token()
            url = f"https://oapi.dingtalk.com/topapi/attendance/getusergroup?access_token={token}"
            payload = {"userid": Config.USER_ID}

            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()

            if data.get("errcode") != 0:
                logger.warning(f"考勤组查询失败: {data.get('errmsg')}")
                return False, f"考勤查询失败: {data.get('errmsg')}"

            group_info = data.get("result", {}).get("group", {})
            schedule_status = group_info.get("schedule_status")

            # schedule_status 可能的值：
            # - WORKING: 工作中
            # - REST: 休息
            # - LEAVE: 请假
            # - TRAVEL: 出差
            if schedule_status == "LEAVE":
                return True, "用户处于请假状态"
            elif schedule_status == "REST":
                return True, "用户处于休息状态"
            elif schedule_status == "TRAVEL":
                return False, "用户出差中（视为在岗）"
            else:
                logger.info(f"考勤状态: {schedule_status or '未知'}，默认视为在岗")
                return False, f"正常在岗（状态: {schedule_status or '未知'}）"

        except Exception as e:
            logger.warning(f"考勤接口异常: {e}，默认放行")
            return False, f"考勤接口异常: {e}"

    # ── 工具接口（初始化用） ───────────────────────────────────

    @classmethod
    def get_userid_by_mobile(cls, mobile: str) -> dict:
        logger.info(f"--- [API Call] 查询 UserID, 手机号: {mobile} ---")
        try:
            token = cls.get_token()
            url = f"https://oapi.dingtalk.com/topapi/v2/user/getbymobile?access_token={token}"
            payload = {"mobile": mobile}

            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()

            if data.get("errcode") == 0:
                return {"success": True, "userid": data.get("result", {}).get("userid")}
            return {"success": False, "error": data.get("errmsg")}
        except Exception as e:
            logger.error(f"❌ 查询 UserID 异常: {e}")
            return {"success": False, "error": str(e)}

    @classmethod
    def get_report_templates(cls, user_id: str) -> dict:
        logger.info(f"--- [API Call] 查询日志模板, UserID: {user_id} ---")
        try:
            token = cls.get_token()
            url = f"https://oapi.dingtalk.com/topapi/report/template/listbyuserid?access_token={token}"
            payload = {"userid": user_id, "offset": 0, "size": 100}

            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()

            if data.get("errcode") == 0:
                raw = data.get("result", {}).get("template_list", [])
                templates = [
                    {
                        "name": t.get("name"),
                        "template_id": t.get("report_code") or t.get("template_id") or t.get("id"),
                    }
                    for t in raw
                ]
                return {"success": True, "templates": templates}
            return {"success": False, "error": data.get("errmsg")}
        except Exception as e:
            logger.error(f"❌ 查询模板异常: {e}")
            return {"success": False, "error": str(e)}


