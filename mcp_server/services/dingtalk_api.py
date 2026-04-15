import json
import time
import traceback

import requests

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("DingTalk_Service")


class DingTalkService:
    _token = None
    _token_expire_time = 0

    @staticmethod
    def _mask_secret(secret: str) -> str:
        """简单的脱敏工具，防止日志泄露核心密钥"""
        if not secret or len(secret) < 6:
            return "***"
        return f"{secret[:3]}***{secret[-3:]}"

    @classmethod
    def get_token(cls) -> str:
        """获取或刷新 Access Token (带本地缓存与详细日志)"""
        logger.debug("--- [API Call] 准备获取钉钉 Token ---")
        logger.debug(f"当前配置 APP_KEY: {Config.APP_KEY}")
        logger.debug(f"当前配置 APP_SECRET (脱敏): {cls._mask_secret(Config.APP_SECRET)}")

        if not Config.APP_KEY or not Config.APP_SECRET:
            logger.error("致命错误: APP_KEY 或 APP_SECRET 为空，请检查 .env 文件！")
            raise ValueError("Missing DingTalk Credentials")

        if cls._token and time.time() < cls._token_expire_time:
            logger.debug("命中本地 Token 缓存，无需重新请求")
            return cls._token

        url = f"https://oapi.dingtalk.com/gettoken?appkey={Config.APP_KEY}&appsecret={Config.APP_SECRET}"
        try:
            logger.debug(f"发送 GET 请求至: https://oapi.dingtalk.com/gettoken")
            response = requests.get(url, timeout=10)
            res_json = response.json()
            logger.debug(f"钉钉返回 Token 响应: {json.dumps(res_json, ensure_ascii=False)}")

            if res_json.get("errcode") == 0:
                cls._token = res_json.get("access_token")
                cls._token_expire_time = time.time() + 7200 - 300
                logger.info("✅ 成功获取并缓存钉钉 Access Token")
                return cls._token
            else:
                logger.error(
                    f"❌ 获取 Token 失败, 错误码: {res_json.get('errcode')}, 错误信息: {res_json.get('errmsg')}")
                raise Exception(f"DingTalk Token Error: {res_json.get('errmsg')}")

        except requests.exceptions.RequestException as req_e:
            logger.error(f"❌ 获取 Token 时发生网络异常: {req_e}")
            logger.debug(traceback.format_exc())
            raise
        except Exception as e:
            logger.error(f"❌ 获取 Token 发生未知异常: {e}")
            logger.debug(traceback.format_exc())
            raise

    @classmethod
    def get_userid_by_mobile(cls, mobile: str) -> dict:
        """根据手机号获取 UserID"""
        logger.info(f"--- [API Call] 开始根据手机号查询 UserID, 手机号: {mobile} ---")
        try:
            token = cls.get_token()
            url = f"https://oapi.dingtalk.com/topapi/v2/user/getbymobile?access_token={token}"
            payload = {"mobile": mobile}

            logger.debug(f"请求 URL: {url.split('?')[0]}?access_token=***")
            logger.debug(f"请求 Payload: {json.dumps(payload, ensure_ascii=False)}")

            response = requests.post(url, json=payload, timeout=10)
            res_json = response.json()
            logger.debug(f"钉钉返回 UserID 响应: {json.dumps(res_json, ensure_ascii=False)}")

            if res_json.get("errcode") == 0:
                user_id = res_json.get("result", {}).get("userid")
                logger.info(f"✅ 成功获取 UserID: {user_id}")
                return {"success": True, "userid": user_id}
            else:
                err_msg = res_json.get("errmsg")
                logger.error(f"❌ 获取 UserID 失败: {err_msg}")
                return {"success": False, "error": err_msg}

        except Exception as e:
            logger.error(f"❌ 查询 UserID 发生代码级异常: {e}")
            logger.debug(traceback.format_exc())
            return {"success": False, "error": str(e)}


    @classmethod
    def get_report_templates(cls, user_id: str) -> dict:
        """获取可见日志模板"""
        logger.info(f"--- [API Call] 开始获取可见日志模板, UserID: {user_id} ---")
        try:
            token = cls.get_token()
            # 【修复点 1】更换为钉钉最新合法的 API 接口
            url = f"https://oapi.dingtalk.com/topapi/report/template/listbyuserid?access_token={token}"

            # 【修复点 2】新接口要求加上分页参数
            payload = {
                "userid": user_id,
                "offset": 0,
                "size": 100
            }

            logger.debug(f"请求 Payload: {json.dumps(payload, ensure_ascii=False)}")
            response = requests.post(url, json=payload, timeout=10)
            res_json = response.json()
            logger.debug(f"钉钉返回日志模板响应: {json.dumps(res_json, ensure_ascii=False)}")

            if res_json.get("errcode") == 0:
                # 【修复点 3】新接口的列表数据嵌套在 result.template_list 中
                templates = res_json.get("result", {}).get("template_list", [])
                result_list = []
                for t in templates:
                    # 钉钉不同版本的模板 ID 字段名可能为 report_code 或 id，做个向下兼容
                    t_id = t.get("report_code") or t.get("template_id") or t.get("id")
                    result_list.append({"name": t.get("name"), "template_id": t_id})

                logger.info(f"✅ 成功获取到 {len(result_list)} 个模板")
                return {"success": True, "templates": result_list}
            else:
                logger.error(f"❌ 获取模板失败: {res_json.get('errmsg')}")
                return {"success": False, "error": res_json.get("errmsg")}
        except Exception as e:
            logger.error(f"❌ 查询模板发生代码级异常: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return {"success": False, "error": str(e)}
