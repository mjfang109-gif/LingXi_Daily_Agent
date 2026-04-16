"""
DingTalkClient — 钉钉单聊消息发送器 + 消息监听

核心能力：
  • send_card_to_user()   — 单聊发送「普通卡片」消息（日志预览）
  • send_text_to_user()   — 单聊发送纯文本（通知/告警）
  • start_message_listener() — 启动消息监听，接收用户回复
  • get_user_response()     — 获取用户回复的关键词（Y/N）

普通卡片（MarkDown 卡片）调用链路：
  POST https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend
  msgType = "markdown"（单聊普通卡片 = markdown 类型 + robotCode）

参考文档：
  https://open.dingtalk.com/document/orgapp/bot-sends-a-single-chat-message
"""
import asyncio
import json
import time
from _asyncio import Task
from typing import Optional

import requests
from flask import Flask, request as flask_request, jsonify

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("DingTalk_Client")

_TOKEN_URL = "https://oapi.dingtalk.com/gettoken"
_SINGLE_SEND_URL = "https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend"

# 全局消息队列，用于存储用户回复
_user_response_queue: asyncio.Queue = asyncio.Queue()


class DingTalkClient:
    """封装钉钉单聊消息发送（机器人），对外暴露卡片 / 文本两种接口"""

    def __init__(self):
        self._token: str | None = None
        self._token_expire_at: float = 0
        self._listener_task: Optional[asyncio.Task] = None

    # ── 属性 ──────────────────────────────────────────────────

    @property
    def is_configured(self) -> bool:
        return bool(Config.CLIENT_ID and Config.CLIENT_SECRET
                    and Config.ROBOT_CODE and Config.USER_ID)

    # ── Token 管理 ────────────────────────────────────────────

    def _get_token(self) -> str | None:
        """获取 AccessToken，本地缓存 115 分钟"""
        if self._token and time.time() < self._token_expire_at:
            return self._token

        resp = requests.get(
            _TOKEN_URL,
            params={"appkey": Config.CLIENT_ID, "appsecret": Config.CLIENT_SECRET},
            timeout=10,
        )
        data = resp.json()
        if data.get("errcode") != 0:
            raise RuntimeError(f"获取钉钉 Token 失败: {data.get('errmsg')}")

        self._token = data["access_token"]
        self._token_expire_at = time.time() + 6900  # 7200s - 5min 缓冲
        logger.info("✅ 钉钉 AccessToken 已刷新并缓存")
        return self._token

    # ── 底层发送 ──────────────────────────────────────────────

    def _send(self, msg_type: str, msg_content: dict) -> dict:
        """
        调用钉钉 batchSend 接口向单个用户发送消息
        文档：https://open.dingtalk.com/document/orgapp/bot-sends-a-single-chat-message
        """
        token = self._get_token()
        payload = {
            "robotCode": Config.ROBOT_CODE,
            "userIds": [Config.USER_ID],
            "msgKey": msg_type,
            "msgParam": json.dumps(msg_content, ensure_ascii=False),
        }
        headers = {
            "Content-Type": "application/json",
            "x-acs-dingtalk-access-token": token,
        }
        logger.debug(f"→ DingTalk batchSend payload: {json.dumps(payload, ensure_ascii=False)[:200]}")

        resp = requests.post(_SINGLE_SEND_URL, json=payload, headers=headers, timeout=10)
        result = resp.json()

        if result.get("processQueryKey"):
            logger.info(f"✅ 消息发送成功，processQueryKey={result['processQueryKey']}")
        else:
            logger.warning(f"⚠️  消息发送响应异常: {result}")

        return result

    # ── 公开接口 ──────────────────────────────────────────────

    def send_card_to_user(
            self,
            title: str,
            today_work: str,
            tomorrow_plan: str,
            summary_card: str,
            countdown_min: int = 15,
            mode: str = "auto",  # "auto" | "manual"
    ) -> bool:
        """
        【核心功能】向用户单聊发送「工作日报预览」普通卡片消息（需求 7/9）

        钉钉普通卡片 = msgKey: "sampleMarkdown"
        卡片内容使用 Markdown 渲染，包含：
          - 今日工作（带状态 Emoji）
          - 明日计划（带状态 Emoji）
          - 任务摘要表格
          - 倒计时提示 + 操作说明
        """
        now_mode_tip = (
            f"⏱ 请在 **{countdown_min} 分钟**内在钉钉回复 **Y** 确认立即发送，超时将自动发送。"
            if mode == "auto"
            else f"⏱ 请在钉钉回复 **Y** 确认发送，或 **N** 取消。"
        )

        # 构造卡片 Markdown 正文
        md_lines = [
            f"## {title}",
            "",
            "### 📋 今日工作",
            today_work.replace("\\n", "\n"),
            "",
            "### 🗓 明日计划",
            tomorrow_plan.replace("\\n", "\n"),
            "",
        ]
        if summary_card:
            md_lines += [
                "### 📊 任务摘要",
                summary_card.replace("\\n", "\n"),
                "",
            ]
        md_lines += [
            "---",
            now_mode_tip,
        ]

        markdown_body = "\n".join(md_lines)

        try:
            self._send(
                msg_type="sampleMarkdown",
                msg_content={
                    "title": title,
                    "text": markdown_body,
                },
            )
            logger.info(f"📨 日报预览卡片已发送给用户 {Config.USER_ID}")
            return True
        except Exception as e:
            logger.error(f"❌ 发送卡片失败: {e}")
            return False

    def send_text_to_user(self, content: str) -> bool:
        """向用户单聊发送纯文本消息（通知/告警用）"""
        try:
            self._send(
                msg_type="sampleText",
                msg_content={"content": content},
            )
            logger.info(f"💬 文本消息已发送: {content[:40]}...")
            return True
        except Exception as e:
            logger.error(f"❌ 发送文本失败: {e}")
            return False

    def send_result_card_to_user(self, success: bool, report_id: str = "", error: str = "") -> bool:
        """
        向用户单聊发送发送结果通知卡片
        成功 → 绿色确认；失败 → 红色告警 + 错误信息
        """
        if success:
            text = (
                f"## ✅ 工作日报发送成功\n\n"
                f"日志 ID：`{report_id}`\n\n"
                f"> 今日工作已记录，收工愉快 🎉"
            )
        else:
            text = (
                f"## 🔥 工作日报发送失败\n\n"
                f"**原因：** `{error}`\n\n"
                f"> 请手动前往钉钉日志提交，或联系管理员排查。"
            )
        try:
            self._send(
                msg_type="sampleMarkdown",
                msg_content={"title": "日报发送结果", "text": text},
            )
            return True
        except Exception as e:
            logger.error(f"❌ 发送结果卡片失败: {e}")
            return False

    # ── 消息监听 ──────────────────────────────────────────────

    def start_message_listener(self, port: int = 8080) -> Task | None:
        """
        启动 HTTP 服务器监听钉钉回调消息

        需要在钉钉开发者后台配置：
        - 消息接收模式：HTTP 回调
        - 消息接收地址：http://your-domain:{port}/dingtalk/callback
        - 加密 aes_key 和签名 secret（可选，此处简化处理）
        """
        app = Flask(__name__)

        @app.route('/dingtalk/callback', methods=['POST'])
        def callback():
            """接收钉钉消息回调"""
            try:
                data = flask_request.get_json()
                logger.debug(f"收到钉钉回调: {json.dumps(data, ensure_ascii=False)}")

                # 提取消息内容
                conversation_id = data.get('conversationId')
                sender_id = data.get('senderId')
                msg_type = data.get('msgtype')

                if msg_type == 'text':
                    text_content = data.get('text', {}).get('content', '').strip().upper()

                    # 只处理目标用户的 Y/N 回复
                    if sender_id == Config.USER_ID and text_content in ['Y', 'N']:
                        logger.info(f"👤 收到用户回复: {text_content}")

                        # 放入异步队列
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(_user_response_queue.put(text_content))
                        loop.close()

                # 返回钉钉要求的响应格式
                return jsonify({"success": True})

            except Exception as e:
                logger.error(f"处理钉钉回调异常: {e}")
                return jsonify({"success": False, "error": str(e)})

        @app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({"status": "ok"}), 200

        def run_flask():
            """在独立线程中运行 Flask"""
            app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

        import threading
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info(f"🌐 钉钉消息监听服务器已启动，端口: {port}")

        async def keep_alive():
            """保持监听任务活跃"""
            while True:
                await asyncio.sleep(60)

        self._listener_task = asyncio.create_task(keep_alive())
        return self._listener_task

    @staticmethod
    async def get_user_response(timeout: float = 0) -> Optional[str]:
        """
        异步获取用户回复

        Args:
            timeout: 超时时间（秒），0 表示非阻塞立即返回

        Returns:
            用户回复内容（Y/N）或 None（超时/无消息）
        """
        try:
            if timeout > 0:
                return await asyncio.wait_for(_user_response_queue.get(), timeout=timeout)
            else:
                return _user_response_queue.get_nowait()
        except (asyncio.TimeoutError, asyncio.QueueEmpty):
            return None
