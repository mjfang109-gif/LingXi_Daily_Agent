"""
DingTalkService — 钉钉底层 API 封装（MCP 层使用）

职责：Token 缓存、日志提交、考勤查询、用户 ID 查询、模板查询
支持多用户：create_report / is_user_on_leave 接受 user_id 参数（需求 14/15）
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
    def get_token(cls) -> str | None:
        """获取 AccessToken，本地缓存 115 分钟"""
        if cls._token and time.time() < cls._token_expire_at:
            return cls._token

        if not Config.CLIENT_ID or not Config.CLIENT_SECRET:
            raise ValueError("缺少 DINGTALK_CLIENT_ID / CLIENT_SECRET")

        url = "https://oapi.dingtalk.com/gettoken"
        params = {"appkey": Config.CLIENT_ID, "appsecret": Config.CLIENT_SECRET}

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
    def create_report(
            cls,
            today_work: str,
            tomorrow_plan: str,
            user_id: str | None = None,
            template_id: str | None = None,
            contents_config: list | None = None,
    ) -> dict:
        """
        提交钉钉工作日志（需求 14/15）
        接口：POST /topapi/report/create

        Args:
            today_work:      今日工作内容（Markdown）
            tomorrow_plan:   明日计划内容（Markdown）
            user_id:         提交人 UserID，缺省用 Config.USER_ID
            template_id:     日志模板 ID，缺省用 Config.TEMPLATE_ID
            contents_config: per-user 字段配置 [{"sort":1,"key":"今日工作"}, ...]
                             缺省用全局 config.yaml 配置
        """
        logger.info("--- [API Call] 提交钉钉工作日志 ---")
        try:
            token = cls.get_token()

            # ── 参数解析（per-user 覆盖全局）──────────────────
            effective_user_id = user_id or Config.USER_ID
            effective_template_id = template_id or Config.TEMPLATE_ID

            if not effective_template_id:
                raise RuntimeError("未配置日志模板 ID（DINGTALK_TEMPLATE_ID 或 per-user template_id）")
            if not effective_user_id:
                raise RuntimeError("未配置用户 ID（DINGTALK_USER_ID 或 per-user user_id）")

            logger.info(f"日志提交：user={effective_user_id}, template={effective_template_id}")

            # ── 构造 contents ──────────────────────────────────
            if contents_config:
                # per-user 自定义字段映射（需求 15）
                contents = []
                field_map = {
                    "今日工作": today_work,
                    "工作内容": today_work,
                    "明日计划": tomorrow_plan,
                    "明日安排": tomorrow_plan,
                }
                for item in contents_config:
                    key = item.get("key", "")
                    content_val = field_map.get(key, "")
                    contents.append({
                        "content_type": "markdown",
                        "sort": item.get("sort", 1),
                        "type": 1,
                        "content": content_val,
                        "key": key,
                    })
            else:
                # 全局默认字段配置
                today_key = Config.get("dingtalk.report_field_today", "今日工作")
                tomorrow_key = Config.get("dingtalk.report_field_tomorrow", "明日计划")
                contents = [
                    {
                        "content_type": "markdown",
                        "sort": 1,
                        "type": 1,
                        "content": today_work,
                        "key": today_key,
                    },
                    {
                        "content_type": "markdown",
                        "sort": 2,
                        "type": 1,
                        "content": tomorrow_plan,
                        "key": tomorrow_key,
                    },
                ]

            dd_from = Config.get("dingtalk.report_dd_from", "report")
            url = f"https://oapi.dingtalk.com/topapi/report/create?access_token={token}"
            payload = {
                "create_report_param": {
                    "contents": contents,
                    "template_id": effective_template_id,
                    "to_chat": False,
                    "dd_from": dd_from,
                    "userid": effective_user_id,
                }
            }

            headers = {"Content-Type": "application/json"}
            logger.debug(f"Payload: {json.dumps(payload, ensure_ascii=False)}")

            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            result = resp.json()

            if result.get("errcode") != 0:
                error_msg = result.get("errmsg", "未知错误")
                raise RuntimeError(
                    f"提交日志失败 (errcode={result.get('errcode')}): {error_msg}"
                )

            report_id = result.get("result", "")
            logger.info(f"✅ 日志提交成功，报告 ID: {report_id}，用户: {effective_user_id}")
            return {"success": True, "report_id": report_id, "data": result}

        except Exception as e:
            logger.error(f"❌ 提交日志异常: {e}")
            logger.debug(traceback.format_exc())
            raise

    # ── 考勤状态 ──────────────────────────────────────────────

    @classmethod
    def is_user_on_leave(cls, user_id: str | None = None) -> tuple[bool, str]:
        """
        查询指定用户是否处于请假状态（需求 6）
        user_id: 缺省使用 Config.USER_ID

        Returns:
            (is_on_leave, reason_str)
        """
        effective_user = user_id or Config.USER_ID
        if not effective_user:
            logger.warning("未配置 USER_ID，跳过考勤查询，默认放行")
            return False, "未配置用户 ID"

        try:
            token = cls.get_token()
            url = f"https://oapi.dingtalk.com/topapi/attendance/getusergroup?access_token={token}"
            payload = {"userid": effective_user}

            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()

            if data.get("errcode") != 0:
                logger.warning(f"考勤组查询失败（用户 {effective_user}）: {data.get('errmsg')}，默认放行")
                return False, f"考勤查询失败: {data.get('errmsg')}"

            group_info = data.get("result", {}).get("group", {})
            schedule_status = group_info.get("schedule_status")

            # WORKING: 工作中 | REST: 休息 | LEAVE: 请假 | TRAVEL: 出差
            if schedule_status == "LEAVE":
                logger.info(f"用户 {effective_user} 处于请假状态")
                return True, "用户处于请假状态"
            elif schedule_status == "REST":
                logger.info(f"用户 {effective_user} 处于休息状态")
                return True, "用户处于休息状态"
            else:
                logger.info(f"用户 {effective_user} 考勤状态: {schedule_status or '未知'}，视为在岗")
                return False, f"正常在岗（状态: {schedule_status or '未知'}）"

        except Exception as e:
            logger.warning(f"考勤接口异常（用户 {effective_user}）: {e}，默认放行")
            return False, f"考勤接口异常: {e}"

    # ── 工具接口（初始化用）───────────────────────────────────

    @classmethod
    def get_userid_by_mobile(cls, mobile: str) -> dict:
        logger.info(f"--- [API Call] 查询 UserID, 手机号: {mobile} ---")
        try:
            token = cls.get_token()
            url = f"https://oapi.dingtalk.com/topapi/v2/user/getbymobile?access_token={token}"
            resp = requests.post(url, json={"mobile": mobile}, timeout=10)
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
            resp = requests.post(
                url,
                json={"userid": user_id, "offset": 0, "size": 100},
                timeout=10,
            )
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
