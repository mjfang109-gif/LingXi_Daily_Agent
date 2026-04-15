import requests
import json
import time
from threading import Lock

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("DingTalk_Client")


class DingTalkClient:
    """
    使用 requests 直接调用钉钉 API 的客户端，用于主动发送企业内部机器人消息。
    - 自动管理 access_token 的获取和刷新。
    - 支持向群聊和个人发送消息。
    """
    def __init__(self):
        self.client_id = Config.CLIENT_ID
        self.client_secret = Config.CLIENT_SECRET
        self.robot_code = Config.ROBOT_CODE
        self.group_chat_id = Config.CHAT_ID
        self.user_id = Config.USER_ID

        self.is_configured = all([self.client_id, self.client_secret, self.robot_code, self.group_chat_id, self.user_id])
        if not self.is_configured:
            logger.warning("钉钉配置不完整，将跳过所有钉钉交互。")
            return

        self._access_token = None
        self._token_expires_at = 0
        self._token_lock = Lock()

    def _get_access_token(self):
        """
        获取并缓存钉钉 access_token，线程安全。
        """
        with self._token_lock:
            # 如果 token 有效，直接返回
            if self._access_token and time.time() < self._token_expires_at:
                return self._access_token

            # 否则，重新获取
            url = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
            payload = {
                "appKey": self.client_id,
                "appSecret": self.client_secret
            }
            headers = {"Content-Type": "application/json"}
            
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if "accessToken" not in data:
                    raise ValueError(f"获取 token 失败: {data}")

                self._access_token = data["accessToken"]
                # expires_in 是秒，设置一个5分钟的缓冲期
                self._token_expires_at = time.time() + data["expireIn"] - 300
                logger.info("成功获取钉钉 Access Token。")
                return self._access_token
            except Exception as e:
                logger.error(f"获取钉钉 Access Token 失败: {e}", exc_info=True)
                self._access_token = None
                return None

    def _send_request(self, url: str, payload: dict):
        """
        统一的 API 请求发送函数。
        """
        if not self.is_configured:
            return

        token = self._get_access_token()
        if not token:
            logger.error("因无法获取 Access Token，消息发送失败。")
            return

        headers = {
            "Content-Type": "application/json",
            "x-acs-dingtalk-access-token": token
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            # 钉钉的业务错误码通常在返回的 JSON 中
            if result.get("errcode") != 0 and "errcode" in result:
                 logger.error(f"钉钉 API 返回业务错误: {result}")
            else:
                 logger.info(f"钉钉消息 API 调用成功: {url}")
        except Exception as e:
            logger.error(f"调用钉钉 API 时出现网络或未知异常: {e}", exc_info=True)

    def send_markdown_to_user(self, title: str, text: str):
        """向指定用户发送 Markdown 预览消息。"""
        url = "https://api.dingtalk.com/v1.0/robot/privateChatMessages/send"
        payload = {
            "msgParam": json.dumps({"title": title, "text": text}),
            "msgKey": "sampleMarkdown",
            "robotCode": self.robot_code,
            "userIds": [self.user_id]
        }
        self._send_request(url, payload)

    def send_text_to_user(self, content: str):
        """向指定用户发送纯文本消息。"""
        url = "https://api.dingtalk.com/v1.0/robot/privateChatMessages/send"
        payload = {
            "msgParam": json.dumps({"content": content}),
            "msgKey": "sampleText",
            "robotCode": self.robot_code,
            "userIds": [self.user_id]
        }
        self._send_request(url, payload)

    def send_markdown_to_group(self, title: str, text: str):
        """向指定群聊发送 Markdown 消息。"""
        url = "https://api.dingtalk.com/v1.0/robot/groupMessages/send"
        payload = {
            "msgParam": json.dumps({"title": title, "text": text}),
            "msgKey": "sampleMarkdown",
            "openConversationId": self.group_chat_id,
            "robotCode": self.robot_code
        }
        self._send_request(url, payload)

    def send_text_to_group(self, content: str):
        """向指定群聊发送纯文本消息。"""
        url = "https://api.dingtalk.com/v1.0/robot/groupMessages/send"
        payload = {
            "msgParam": json.dumps({"content": content}),
            "msgKey": "sampleText",
            "openConversationId": self.group_chat_id,
            "robotCode": self.robot_code
        }
        self._send_request(url, payload)
