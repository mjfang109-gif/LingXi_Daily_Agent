"""
DingTalkMessageService — 钉钉消息服务（MCP 层）

架构（需求 10/13）：
  - 机器人通过 dingtalk-stream SDK 建立 WebSocket 长连接接收消息，无需回调地址
  - 接收消息：WebSocket Stream 纯粹负责接收，具体业务逻辑通过回调（Callback）交还给 Agent 层处理
  - 发送消息：HTTP API（batchSend），支持多用户（需求 14）
"""
import json
import threading
import time
import requests

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("DingTalk_Message_Service")

_TOKEN_URL = "https://oapi.dingtalk.com/gettoken"
_SINGLE_SEND_URL = "https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend"


class DingTalkMessageService:
    """封装钉钉消息发送（HTTP）和接收（WebSocket Stream）"""

    _token: str | None = None
    _token_expire_at: float = 0
    _stream_client = None
    _stream_thread: threading.Thread | None = None

    @classmethod
    def _get_token(cls) -> str | None:
        """获取 AccessToken，本地缓存 115 分钟"""
        if cls._token and time.time() < cls._token_expire_at:
            return cls._token

        if not Config.CLIENT_ID or not Config.CLIENT_SECRET:
            raise ValueError("缺少 DINGTALK_CLIENT_ID / CLIENT_SECRET")

        resp = requests.get(
            _TOKEN_URL,
            params={"appkey": Config.CLIENT_ID, "appsecret": Config.CLIENT_SECRET},
            timeout=10,
        )
        data = resp.json()
        if data.get("errcode") != 0:
            raise RuntimeError(f"获取钉钉 Token 失败: {data.get('errmsg')}")

        cls._token = data["access_token"]
        cls._token_expire_at = time.time() + 6900  # 7200s - 5min 缓冲
        logger.info("✅ 钉钉 AccessToken 已刷新并缓存")
        return cls._token

    @classmethod
    def _send(cls, msg_type: str, msg_content: dict, user_id: str | None = None) -> dict:
        """调用钉钉 batchSend 接口向指定用户发送消息（支持多用户）"""
        target_user = user_id or Config.USER_ID
        if not target_user:
            raise ValueError("未指定目标用户 user_id，请配置 DINGTALK_USER_ID 或传入 user_id")

        token = cls._get_token()
        payload = {
            "robotCode": Config.ROBOT_CODE,
            "userIds": [target_user],
            "msgKey": msg_type,
            "msgParam": json.dumps(msg_content, ensure_ascii=False),
        }
        headers = {
            "Content-Type": "application/json",
            "x-acs-dingtalk-access-token": token,
        }

        logger.debug(f"→ DingTalk batchSend to={target_user}: {str(payload)[:200]}")
        resp = requests.post(_SINGLE_SEND_URL, json=payload, headers=headers, timeout=10)
        result = resp.json()

        if result.get("processQueryKey"):
            logger.info(f"✅ 消息发送成功 → {target_user}")
        else:
            logger.warning(f"⚠️  消息发送响应异常: {result}")

        return result

    @classmethod
    def send_text_to_user(cls, content: str, user_id: str | None = None) -> bool:
        """向用户单聊发送纯文本消息"""
        try:
            cls._send("sampleText", {"content": content}, user_id=user_id)
            return True
        except Exception as e:
            logger.error(f"❌ 发送文本失败: {e}")
            return False

    @classmethod
    def send_card_to_user(
            cls, title: str, today_work: str, tomorrow_plan: str,
            summary_card: str = "", countdown_min: int = 15,
            mode: str = "auto", user_id: str | None = None,
    ) -> bool:
        """支持 preview 纯净预览模式"""

        if mode == "preview":
            mode_tip = "💡 **实时预览卡片**：仅供查看，此状态下回复任何内容均**不会**触发实际发送。"
        elif mode == "auto":
            mode_tip = f"⏱ 请在 **{countdown_min} 分钟**内回复 **Y** 确认立即发送，超时将自动发送。"
        else:
            mode_tip = "⏱ 请回复 **Y** 确认发送，或 **N** 取消。"

        md_lines = [
            f"## {title}", "",
            "### 📋 今日工作", today_work.replace("\\n", "\n"), "",
            "### 🗓 明日计划", tomorrow_plan.replace("\\n", "\n"), "",
        ]
        if summary_card:
            md_lines += ["### 📊 任务摘要", summary_card.replace("\\n", "\n"), ""]
        md_lines += ["---", mode_tip]

        try:
            cls._send("sampleMarkdown", {"title": title, "text": "\n".join(md_lines)}, user_id=user_id)
            return True
        except Exception as e:
            logger.error(f"❌ 发送卡片失败: {e}")
            return False

    @classmethod
    def send_result_card_to_user(
            cls, success: bool, report_id: str = "", error: str = "", user_id: str | None = None,
    ) -> bool:
        """向用户单聊发送日报发送结果通知卡片"""
        if success:
            text = f"## ✅ 工作日报发送成功\n\n日志 ID：`{report_id}`\n\n> 今日工作已记录，收工愉快 🎉"
        else:
            text = f"## 🔥 工作日报发送失败\n\n**原因：** `{error}`\n\n> 请手动前往钉钉日志提交，或联系管理员排查。"
        try:
            cls._send("sampleMarkdown", {"title": "日报发送结果", "text": text}, user_id=user_id)
            return True
        except Exception as e:
            logger.error(f"❌ 发送结果卡片失败: {e}")
            return False

    @classmethod
    def start_message_listener(cls, on_message_callback) -> None:
        """
        启动钉钉 Stream WebSocket 长连接监听（核心修复）。
        参数 on_message_callback: 接收到消息时的回调函数，由 Agent 层传入。
        """
        if cls._stream_client is not None:
            logger.warning("Stream 监听器已启动，跳过重复初始化")
            return

        try:
            import dingtalk_stream
            from dingtalk_stream import AckMessage
        except ImportError:
            logger.error("❌ dingtalk-stream 未安装，请执行: pip install dingtalk-stream")
            raise

        class _BotMessageHandler(dingtalk_stream.ChatbotHandler):
            async def process(self, callback: dingtalk_stream.CallbackMessage):
                try:
                    incoming = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
                    sender_id = incoming.sender_staff_id
                    raw_text = (incoming.text.content or "").strip()

                    logger.debug(f"[Stream] 收到消息 from={sender_id}: {raw_text}")

                    if raw_text and sender_id:
                        # 彻底解耦：通过回调将原始数据交还给 Agent 大脑进行业务处理
                        on_message_callback(sender_id, raw_text)

                    # 必须返回成功回执，否则钉钉网关会不断重试
                    return AckMessage.STATUS_OK, 'OK'
                except Exception as e:
                    logger.error(f"❌ Stream 消息处理异常: {e}", exc_info=True)
                    return AckMessage.STATUS_OK, 'OK'

        credential = dingtalk_stream.Credential(Config.CLIENT_ID, Config.CLIENT_SECRET)
        client = dingtalk_stream.DingTalkStreamClient(credential)
        client.register_callback_handler(dingtalk_stream.ChatbotMessage.TOPIC, _BotMessageHandler())

        def _run_stream():
            logger.info("📡 钉钉 Stream WebSocket 监听已启动（等待消息...）")
            try:
                client.start_forever()
            except Exception as e:
                logger.error(f"❌ Stream 客户端异常退出: {e}", exc_info=True)

        thread = threading.Thread(target=_run_stream, daemon=True, name="DingTalkStream")
        thread.start()

        cls._stream_client = client
        cls._stream_thread = thread
        logger.info("✅ Stream 监听线程已启动（WebSocket 长连接，无回调地址）")
