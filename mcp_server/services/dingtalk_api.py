"""
DingTalkService — 钉钉底层 API 封装（MCP 层使用）

职责：Token 缓存、日志提交、考勤查询、用户 ID 查询、模板查询
支持多用户：create_report / is_user_on_leave 接受 user_id 参数（需求 14/15）
"""
import json
import threading
import time
import traceback

import requests

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("DingTalk_Service")


class DingTalkService:
    _token: str | None = None
    _token_expire_at: float = 0
    _token_lock: threading.Lock = threading.Lock()  # 用于保护 Token 刷新的线程锁

    @staticmethod
    def _mask(secret: str) -> str:
        """脱敏敏感信息，用于日志打印"""
        if not secret or len(secret) < 6:
            return "***"
        return f"{secret[:3]}***{secret[-3:]}"

    # ── Token ─────────────────────────────────────────────────

    @classmethod
    def get_token(cls) -> str | None:
        """
        获取 AccessToken，本地缓存 115 分钟
        :return: access_token string
        """
        # 双重检查锁定（Double-Checked Locking）避免并发刷新
        if cls._token and time.time() < cls._token_expire_at:
            logger.debug("使用缓存的 DingTalk AccessToken")
            return cls._token

        # 使用锁保护 Token 刷新过程
        with cls._token_lock:
            # 再次检查，防止多个线程同时等待锁后重复刷新
            if cls._token and time.time() < cls._token_expire_at:
                logger.debug("使用缓存的 DingTalk AccessToken (锁内检查)")
                return cls._token

            logger.info("--- [API Call] 获取钉钉 AccessToken ---")

            if not Config.CLIENT_ID or not Config.CLIENT_SECRET:
                logger.error("配置缺失: DINGTALK_CLIENT_ID 或 CLIENT_SECRET 未配置")
                raise ValueError("缺少 DINGTALK_CLIENT_ID / CLIENT_SECRET")

            url = "https://oapi.dingtalk.com/gettoken"
            params = {
                "appkey": Config.CLIENT_ID,
                "appsecret": Config.CLIENT_SECRET
            }

            # 日志中脱敏显示密钥
            logger.debug(f"请求参数: appkey={cls._mask(Config.CLIENT_ID)}, appsecret={cls._mask(Config.CLIENT_SECRET)}")

            try:
                resp = requests.get(url, params=params, timeout=10)
                data = resp.json()

                logger.debug(f"响应数据: {json.dumps(data, ensure_ascii=False)}")

                if data.get("errcode") != 0:
                    error_msg = data.get('errmsg', 'Unknown Error')
                    logger.error(f"Token 获取失败 (errcode={data.get('errcode')}): {error_msg}")
                    raise RuntimeError(f"Token 获取失败: {error_msg}")

                cls._token = data["access_token"]
                # 7200s - 5min (300s) 缓冲 = 6900s
                cls._token_expire_at = time.time() + 6900
                logger.info("✅ DingTalk AccessToken 已刷新并缓存")
                return cls._token

            except Exception as e:
                logger.error(f"❌ 获取 Token 异常: {e}")
                logger.debug(traceback.format_exc())
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
        
        Returns:
            dict: {"success": True, "report_id": "...", "data": {...}}
        """
        logger.info("--- [API Call] 提交钉钉工作日志 ---")
        logger.info(
            f"入参: today_work={today_work}, tomorrow_plan={tomorrow_plan}, user_id={user_id}, template_id={template_id}")

        try:
            token = cls.get_token()

            # ── 参数解析（per-user 覆盖全局）──────────────────
            effective_user_id = user_id or Config.USER_ID
            effective_template_id = template_id or Config.TEMPLATE_ID

            if not effective_template_id:
                logger.error("未配置日志模板 ID")
                raise RuntimeError("未配置日志模板 ID（DINGTALK_TEMPLATE_ID 或 per-user template_id）")
            if not effective_user_id:
                logger.error("未配置用户 ID")
                raise RuntimeError("未配置用户 ID（DINGTALK_USER_ID 或 per-user user_id）")

            logger.info(f"最终执行参数: user={effective_user_id}, template={effective_template_id}")

            # ── 构造 contents ──────────────────────────────────
            if contents_config:
                logger.debug(f"使用自定义字段配置: {contents_config}")
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
                logger.debug("使用全局默认字段配置")
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
            url = f"https://oapi.dingtalk.com/topapi/report/create?access_token={cls._mask(token)}"
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
            logger.debug(f"请求 URL: {url}")
            logger.debug(f"请求 Payload: {json.dumps(payload, ensure_ascii=False)}")

            resp = requests.post(url.replace(cls._mask(token), token), json=payload, headers=headers, timeout=15)
            result = resp.json()

            logger.debug(f"响应数据: {json.dumps(result, ensure_ascii=False)}")

            if result.get("errcode") != 0:
                error_msg = result.get("errmsg", "未知错误")
                logger.error(f"提交日志失败 (errcode={result.get('errcode')}): {error_msg}")
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
        logger.info(f"--- [API Call] 查询用户考勤状态, User: {effective_user} ---")

        if not effective_user:
            logger.warning("未配置 USER_ID，跳过考勤查询，默认放行")
            return False, "未配置用户 ID"

        try:
            token = cls.get_token()
            url = f"https://oapi.dingtalk.com/topapi/attendance/getusergroup?access_token={cls._mask(token)}"
            payload = {"userid": effective_user}

            logger.debug(f"请求 Payload: {json.dumps(payload, ensure_ascii=False)}")

            resp = requests.post(url.replace(cls._mask(token), token), json=payload, timeout=10)
            data = resp.json()

            logger.debug(f"响应数据: {json.dumps(data, ensure_ascii=False)}")

            if data.get("errcode") != 0:
                err_msg = data.get('errmsg', 'Unknown')
                logger.warning(f"考勤组查询失败（用户 {effective_user}）: {err_msg}，默认放行")
                return False, f"考勤查询失败: {err_msg}"

            group_info = data.get("result", {}).get("group", {})
            schedule_status = group_info.get("schedule_status")

            logger.info(f"用户 {effective_user} 原始考勤状态码: {schedule_status}")

            # WORKING: 工作中 | REST: 休息 | LEAVE: 请假 | TRAVEL: 出差
            if schedule_status == "LEAVE":
                logger.info(f"判定结果: 用户 {effective_user} 处于请假状态")
                return True, "用户处于请假状态"
            elif schedule_status == "REST":
                logger.info(f"判定结果: 用户 {effective_user} 处于休息状态")
                return True, "用户处于休息状态"
            else:
                logger.info(f"判定结果: 用户 {effective_user} 视为在岗（状态: {schedule_status or '未知'}）")
                return False, f"正常在岗（状态: {schedule_status or '未知'}）"

        except Exception as e:
            logger.warning(f"考勤接口异常（用户 {effective_user}）: {e}，默认放行")
            logger.debug(traceback.format_exc())
            return False, f"考勤接口异常: {e}"

    # ── 工具接口（初始化用）───────────────────────────────────

    @classmethod
    def get_userid_by_mobile(cls, mobile: str) -> dict:
        """
        根据手机号查询钉钉 UserID
        :param mobile: 手机号
        :return: dict with success status and userid
        """
        logger.info(f"--- [API Call] 查询 UserID, 手机号: {mobile} ---")
        logger.debug(f"入参: mobile={mobile}")
        try:
            token = cls.get_token()
            url = f"https://oapi.dingtalk.com/topapi/v2/user/getbymobile?access_token={cls._mask(token)}"
            payload = {"mobile": mobile}

            logger.debug(f"请求 Payload: {json.dumps(payload, ensure_ascii=False)}")

            resp = requests.post(url.replace(cls._mask(token), token), json=payload, timeout=10)
            data = resp.json()

            logger.debug(f"响应数据: {json.dumps(data, ensure_ascii=False)}")

            if data.get("errcode") == 0:
                userid = data.get("result", {}).get("userid")
                logger.info(f"✅ 查询成功, UserID: {userid}")
                return {"success": True, "userid": userid}
            else:
                logger.warning(f"查询失败: {data.get('errmsg')}")
                return {"success": False, "error": data.get("errmsg")}
        except Exception as e:
            logger.error(f"❌ 查询 UserID 异常: {e}")
            logger.debug(traceback.format_exc())
            return {"success": False, "error": str(e)}

    @classmethod
    def get_report_templates(cls, user_id: str) -> dict:
        """
        查询用户的日志模板列表
        :param user_id: 钉钉 UserID
        :return: dict with success status and templates list
        """
        logger.info(f"--- [API Call] 查询日志模板, UserID: {user_id} ---")
        logger.debug(f"入参: user_id={user_id}")
        try:
            token = cls.get_token()
            url = f"https://oapi.dingtalk.com/topapi/report/template/listbyuserid?access_token={cls._mask(token)}"
            payload = {"userid": user_id, "offset": 0, "size": 100}

            logger.debug(f"请求 Payload: {json.dumps(payload, ensure_ascii=False)}")

            resp = requests.post(url.replace(cls._mask(token), token), json=payload, timeout=10)
            data = resp.json()

            logger.debug(f"响应数据: {json.dumps(data, ensure_ascii=False)}")

            if data.get("errcode") == 0:
                raw = data.get("result", {}).get("template_list", [])
                templates = []
                for t in raw:
                    # 尝试从多个可能的字段名中获取 template_id
                    # 根据实际测试，钉钉API返回的字段名为 template_id
                    tmpl_id = t.get("template_id")

                    tmpl_name = t.get("name") or t.get("template_name")

                    templates.append({
                        "name": tmpl_name,
                        "template_id": tmpl_id,
                        # 保留原始数据以便调试
                        "_raw": t
                    })

                logger.info(f"✅ 查询到 {len(templates)} 个模板")
                logger.debug(f"模板详情: {json.dumps(templates, ensure_ascii=False, indent=2)}")
                return {"success": True, "templates": templates}
            else:
                logger.warning(f"查询模板失败: {data.get('errmsg')}")
                return {"success": False, "error": data.get("errmsg")}
        except Exception as e:
            logger.error(f"❌ 查询模板异常: {e}")
            logger.debug(traceback.format_exc())
            return {"success": False, "error": str(e)}

    @classmethod
    def get_template_detail(cls, user_id: str, template_id: str) -> dict:
        """
        查询指定模板的详细信息（包含字段结构）
        接口：POST /topapi/report/template/getbyname

        Args:
            user_id: 钉钉 UserID
            template_id: 模板 ID

        Returns:
            {
                "success": True,
                "template_name": "日常日报",
                "contents": [
                    {"key": "今日工作", "sort": 1, "type": "markdown"},
                    {"key": "明日计划", "sort": 2, "type": "markdown"}
                ]
            }
        """
        logger.info(f"--- [API Call] 查询模板详情, UserID: {user_id}, TemplateID: {template_id} ---")
        logger.debug(f"入参: user_id={user_id}, template_id={template_id}")

        try:
            token = cls.get_token()

            # 第一步：从 UserStore 缓存中获取模板名称
            from common.user_store import UserStore

            all_templates = UserStore.get_all_templates(user_id)
            template_name = None

            if template_id in all_templates:
                template_name = all_templates[template_id].get("name")
                logger.info(f"✅ 从缓存中找到模板名称: {template_name}")

            if not template_name:
                logger.warning(f"缓存中未找到模板 {template_id}，尝试从 API 重新获取模板列表")
                # 重新查询模板列表获取名称
                list_result = cls.get_report_templates(user_id)
                if list_result.get("success"):
                    for tmpl in list_result.get("templates", []):
                        if tmpl.get("template_id") == template_id:
                            template_name = tmpl.get("name")
                            break

            if not template_name:
                logger.error(f"无法获取模板 {template_id} 的名称，使用配置兜底")
                # 降级方案：使用配置文件中的默认字段
                from common.config_loader import Config

                today_key = Config.get("dingtalk.report_field_today", "今日工作")
                tomorrow_key = Config.get("dingtalk.report_field_tomorrow", "明日计划")

                contents = [
                    {"key": today_key, "sort": 1, "type": 1, "content_type": "markdown"},
                    {"key": tomorrow_key, "sort": 2, "type": 1, "content_type": "markdown"},
                ]

                return {
                    "success": True,
                    "template_name": "默认模板",
                    "contents": contents,
                }

            logger.info(f"模板名称: {template_name}")

            # 第二步：使用 getbyname 接口获取模板详情
            url = f"https://oapi.dingtalk.com/topapi/report/template/getbyname?access_token={cls._mask(token)}"
            payload = {"userid": user_id, "template_name": template_name}

            logger.debug(f"请求 Payload: {json.dumps(payload, ensure_ascii=False)}")

            resp = requests.post(url.replace(cls._mask(token), token), json=payload, timeout=10)
            data = resp.json()

            logger.debug(f"响应数据: {json.dumps(data, ensure_ascii=False)}")

            if data.get("errcode") == 0:
                result = data.get("result", {})
                template_name = result.get("name", "")

                # 提取字段结构 - 钉钉 API 返回的是 fields 而不是 contents
                contents_raw = result.get("fields", []) or result.get("contents", [])
                contents = []
                for item in contents_raw:
                    # 兼容两种字段名：field_name 或 key
                    field_key = item.get("field_name") or item.get("key", "")
                    contents.append({
                        "key": field_key,
                        "sort": item.get("sort", 0),
                        "type": item.get("type", 1),
                        "content_type": "markdown",
                    })

                # 按 sort 排序
                contents.sort(key=lambda x: x["sort"])

                logger.info(f"✅ 模板 '{template_name}' 包含 {len(contents)} 个字段")
                logger.debug(f"字段详情: {contents}")
                return {
                    "success": True,
                    "template_name": template_name,
                    "contents": contents,
                }
            else:
                logger.warning(f"模板详情查询失败: {data.get('errmsg')}，使用配置兜底")
                # API 失败时的降级方案
                from common.config_loader import Config

                today_key = Config.get("dingtalk.report_field_today", "今日工作")
                tomorrow_key = Config.get("dingtalk.report_field_tomorrow", "明日计划")

                contents = [
                    {"key": today_key, "sort": 1, "type": 1, "content_type": "markdown"},
                    {"key": tomorrow_key, "sort": 2, "type": 1, "content_type": "markdown"},
                ]

                return {
                    "success": True,
                    "template_name": template_name,
                    "contents": contents,
                }

        except Exception as e:
            logger.error(f"❌ 查询模板详情异常: {e}")
            logger.debug(traceback.format_exc())
            # 异常时的降级方案
            from common.config_loader import Config

            today_key = Config.get("dingtalk.report_field_today", "今日工作")
            tomorrow_key = Config.get("dingtalk.report_field_tomorrow", "明日计划")

            return {
                "success": True,
                "template_name": "默认模板",
                "contents": [
                    {"key": today_key, "sort": 1, "type": 1, "content_type": "markdown"},
                    {"key": tomorrow_key, "sort": 2, "type": 1, "content_type": "markdown"},
                ],
            }
