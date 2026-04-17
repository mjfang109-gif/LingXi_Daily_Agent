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
        """
        获取 AccessToken，本地缓存 115 分钟。
        
        Returns:
            str: 有效的 access_token
        Raises:
            ValueError: 配置缺失
            RuntimeError: API 调用失败
        """
        # 检查缓存是否有效
        if cls._token and time.time() < cls._token_expire_at:
            logger.debug(f"🔄 使用缓存的 AccessToken (剩余有效期: {cls._token_expire_at - time.time():.0f}s)")
            return cls._token

        # 校验配置
        if not Config.CLIENT_ID or not Config.CLIENT_SECRET:
            logger.error("❌ 配置错误: 缺少 DINGTALK_CLIENT_ID 或 CLIENT_SECRET")
            raise ValueError("缺少 DINGTALK_CLIENT_ID / CLIENT_SECRET")

        logger.info("🔑 开始请求新的钉钉 AccessToken...")
        try:
            resp = requests.get(
                _TOKEN_URL,
                params={"appkey": Config.CLIENT_ID, "appsecret": Config.CLIENT_SECRET},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()

            logger.debug(f"📥 Token API 响应: errcode={data.get('errcode')}, errmsg={data.get('errmsg')}")

            if data.get("errcode") != 0:
                error_msg = data.get('errmsg', 'Unknown Error')
                logger.error(f"❌ 获取钉钉 Token 失败: errcode={data.get('errcode')}, errmsg={error_msg}")
                raise RuntimeError(f"获取钉钉 Token 失败: {error_msg}")

            cls._token = data["access_token"]
            # 7200s (2小时) - 300s (5分钟缓冲) = 6900s
            cls._token_expire_at = time.time() + 6900

            logger.info(
                f"✅ 钉钉 AccessToken 已刷新并缓存 (Expires At: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cls._token_expire_at))})")
            return cls._token

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 请求钉钉 Token API 网络异常: {e}")
            raise RuntimeError(f"请求钉钉 Token API 失败: {e}")

    @classmethod
    def _send(cls, msg_type: str, msg_content: dict, user_id: str | None = None) -> dict:
        """
        调用钉钉 batchSend 接口向指定用户发送消息（支持多用户）。
        
        Args:
            msg_type (str): 消息类型 key (如 sampleText, sampleMarkdown)
            msg_content (dict): 消息内容字典
            user_id (str, optional): 目标用户 ID，若为空则使用配置中的默认用户
            
        Returns:
            dict: 钉钉 API 响应结果
            
        Raises:
            ValueError: 未指定目标用户
        """
        target_user = user_id or Config.USER_ID
        if not target_user:
            logger.error("❌ 参数错误: 未指定目标用户 user_id，且配置中无 DINGTALK_USER_ID")
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

        logger.info(f"🚀 准备发送钉钉消息 | Type: {msg_type} | To: {target_user} | Robot: {Config.ROBOT_CODE}")
        logger.debug(f"📤 请求 Payload: {json.dumps(payload, ensure_ascii=False)}")

        try:
            resp = requests.post(_SINGLE_SEND_URL, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()
            result = resp.json()

            logger.debug(f"📥 响应 Result: {json.dumps(result, ensure_ascii=False)}")

            # processQueryKey 存在通常表示异步任务已提交成功
            if result.get("processQueryKey"):
                logger.info(f"✅ 消息发送请求已接受 | ProcessKey: {result.get('processQueryKey')} | To: {target_user}")
            else:
                logger.warning(f"⚠️ 消息发送响应异常 (无 processQueryKey): {result}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 发送消息 HTTP 请求失败: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ 发送消息处理异常: {e}", exc_info=True)
            raise

    @classmethod
    def send_text_to_user(cls, content: str, user_id: str | None = None) -> bool:
        """
        向用户单聊发送纯文本消息。
        
        Args:
            content (str): 文本内容
            user_id (str, optional): 目标用户 ID
            
        Returns:
            bool: 发送是否成功
        """
        logger.info(f"📝 [SendText] 准备发送文本消息 | Len: {len(content)} | User: {user_id or Config.USER_ID}")
        try:
            cls._send("sampleText", {"content": content}, user_id=user_id)
            logger.info(f"✅ [SendText] 文本消息发送流程完成")
            return True
        except Exception as e:
            logger.error(f"❌ [SendText] 发送文本失败: {e}", exc_info=True)
            return False

    @classmethod
    def send_card_to_user(
            cls, title: str, today_work: str, tomorrow_plan: str,
            countdown_min: int = 15,
            mode: str = "auto", user_id: str | None = None,
    ) -> bool:
        """
        向用户发送 Markdown 格式的工作日报卡片，支持预览模式。

        Args:
            title (str): 卡片标题
            today_work (str): 今日工作内容
            tomorrow_plan (str): 明日计划
            countdown_min (int): 自动发送倒计时分钟数
            mode (str): 模式 ('preview', 'auto', 'manual')
            user_id (str, optional): 目标用户 ID

        Returns:
            bool: 发送是否成功
        """
        logger.info(f"[SendCard] ========== 开始发送卡片 ==========")
        logger.info(f"[SendCard] 参数: Mode={mode}, Title={title}, User={user_id or Config.USER_ID}")
        logger.info(f"[SendCard] 内容长度: Today={len(today_work)}, Tomorrow={len(tomorrow_plan)}")

        # 检查必要参数
        if not user_id and not Config.USER_ID:
            logger.error("❌ [SendCard] 错误: 未指定 user_id 且 Config.USER_ID 为空")
            return False

        if mode == "preview":
            mode_tip = "**实时预览卡片**：仅供查看，此状态下回复任何内容均**不会**触发实际发送。"
            logger.info("[SendCard] 模式: 预览模式 (Preview)")
        elif mode == "auto":
            mode_tip = f"请在 **{countdown_min} 分钟**内回复 **Y** 确认立即发送，超时将自动发送。"
            logger.info(f"[SendCard] 模式: 自动模式 (Auto, 倒计时: {countdown_min}min)")
        else:
            mode_tip = "请回复 **Y** 确认发送，或 **N** 取消。"
            logger.info("[SendCard] 模式: 手动确认模式 (Manual)")

        # 处理换行：确保每行末尾有两个空格（Markdown 硬换行语法）
        def format_markdown_lines(text: str) -> str:
            if not text:
                return ""
            # 先统一换行符格式
            text = text.replace("\\n", "\n")
            # 为每一行添加两个空格以实现 Markdown 硬换行
            lines = text.split("\n")
            formatted_lines = []
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                # 检测是否为分类标题（以"一、"、"二、"等中文数字开头）
                import re
                if re.match(r'^[一二三四五六七八九十]+、', stripped):
                    # 分类标题加粗显示
                    formatted_lines.append(f"**{stripped}**  ")
                else:
                    # 普通任务行
                    formatted_lines.append(stripped + "  ")
            return "\n".join(formatted_lines)

        md_lines = [
            f"## {title}",
            "",
            "### **今日工作**",
            "",
            format_markdown_lines(today_work),
            "",
            "---",
            "",
            "### **明日计划**",
            "",
            format_markdown_lines(tomorrow_plan),
            "",
        ]

        md_lines += ["---", mode_tip]

        final_markdown = "\n".join(md_lines)
        logger.info(f"[SendCard] Markdown 生成完成，总长度: {len(final_markdown)} 字符")

        try:
            logger.info(f"[SendCard] 准备调用 _send 方法...")

            result = cls._send("sampleMarkdown", {"title": title, "text": final_markdown}, user_id=user_id)

            logger.info(f"[SendCard] _send 方法返回: {result}")
            logger.info(f"✅ [SendCard] 卡片消息发送成功")
            logger.info(f"[SendCard] ========== 发送完成 ==========")
            return True

        except Exception as e:
            logger.error(f"❌ [SendCard] 发送卡片异常")
            logger.error(f"   错误类型: {type(e).__name__}")
            logger.error(f"   错误消息: {str(e)}")

            import traceback
            tb_str = traceback.format_exc()
            logger.error(f"   堆栈跟踪:\n{tb_str}")

            logger.info(f"[SendCard] ========== 发送失败 ==========")
            return False

    @classmethod
    def send_result_card_to_user(
            cls, success: bool, report_id: str = "", error: str = "", user_id: str | None = None,
    ) -> bool:
        """
        向用户单聊发送日报发送结果通知卡片。
        
        Args:
            success (bool): 是否成功
            report_id (str, optional): 报告 ID
            error (str, optional): 错误信息
            user_id (str, optional): 目标用户 ID
            
        Returns:
            bool: 发送是否成功
        """
        status = "Success" if success else "Failed"
        logger.info(
            f"📢 [ResultCard] 准备发送结果通知 | Status: {status} | ReportID: {report_id} | User: {user_id or Config.USER_ID}")

        if success:
            text = f"## ✅ 工作日报发送成功\n\n日志 ID：`{report_id}`\n\n> 今日工作已记录，收工愉快 🎉"
        else:
            logger.warning(f"⚠️ [ResultCard] 因失败发送通知, 错误原因: {error}")
            text = f"## 🔥 工作日报发送失败\n\n**原因：** `{error}`\n\n> 请手动前往钉钉日志提交，或联系管理员排查。"

        try:
            cls._send("sampleMarkdown", {"title": "日报发送结果", "text": text}, user_id=user_id)
            logger.info(f"✅ [ResultCard] 结果通知发送流程完成")
            return True
        except Exception as e:
            logger.error(f"❌ [ResultCard] 发送结果卡片失败: {e}", exc_info=True)
            return False

    @classmethod
    def start_message_listener(cls, on_message_callback) -> None:
        """
        启动钉钉 Stream WebSocket 长连接监听（核心修复）。
        
        Args:
            on_message_callback (callable): 接收到消息时的回调函数 (sender_id, raw_text)，由 Agent 层传入。
        """
        if cls._stream_client is not None:
            logger.warning("⚠️ Stream 监听器已启动，跳过重复初始化")
            return

        logger.info("🔌 正在初始化钉钉 Stream WebSocket 客户端...")

        try:
            import dingtalk_stream
            from dingtalk_stream import AckMessage
        except ImportError:
            logger.error("❌ 依赖缺失: dingtalk-stream 未安装，请执行: pip install dingtalk-stream")
            raise

        class _BotMessageHandler(dingtalk_stream.ChatbotHandler):
            """内部类：处理钉钉 Stream 消息回调"""

            async def process(self, callback: dingtalk_stream.CallbackMessage):
                try:
                    # 解析原始数据
                    incoming = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
                    sender_id = incoming.sender_staff_id
                    raw_text = (incoming.text.content or "").strip()

                    # 详细日志：入参
                    logger.debug(
                        f"📥 [Stream Handler] 收到原始回调数据 | Sender: {sender_id} | Content: '{raw_text}' | Data: {callback.data}")

                    if raw_text and sender_id:
                        logger.info(f"💬 [Stream] 触发业务回调 | From: {sender_id} | Text: {raw_text}")
                        # 彻底解耦：通过回调将原始数据交还给 Agent 大脑进行业务处理
                        try:
                            on_message_callback(sender_id, raw_text)
                            logger.debug(f"✅ [Stream] 业务回调执行完毕")
                        except Exception as cb_err:
                            logger.error(f"❌ [Stream] 用户提供的回调函数执行异常: {cb_err}", exc_info=True)
                    else:
                        logger.debug(f"⚪ [Stream] 忽略空消息或无发送者ID的消息")

                    # 必须返回成功回执，否则钉钉网关会不断重试
                    return AckMessage.STATUS_OK, 'OK'

                except Exception as e:
                    logger.error(f"❌ [Stream Handler] 消息处理顶层异常: {e}", exc_info=True)
                    # 即使出错也返回 OK，避免钉钉重试风暴，具体错误已在日志中记录
                    return AckMessage.STATUS_OK, 'OK'

        # 创建凭证和客户端
        logger.debug(f"🔑 [Stream] 使用 ClientID: {Config.CLIENT_ID} 创建 Credential")
        credential = dingtalk_stream.Credential(Config.CLIENT_ID, Config.CLIENT_SECRET)
        client = dingtalk_stream.DingTalkStreamClient(credential)

        # 注册回调处理器
        client.register_callback_handler(dingtalk_stream.ChatbotMessage.TOPIC, _BotMessageHandler())
        logger.info("📝 [Stream] 回调处理器已注册")

        def _run_stream():
            logger.info("📡 [Stream Thread] 钉钉 Stream WebSocket 监听线程已启动，开始等待消息...")
            try:
                client.start_forever()
            except Exception as e:
                logger.error(f"❌ [Stream Thread] Stream 客户端异常退出: {e}", exc_info=True)

        # 启动后台线程
        thread = threading.Thread(target=_run_stream, daemon=True, name="DingTalkStreamListener")
        thread.start()

        # 保存引用
        cls._stream_client = client
        cls._stream_thread = thread

        logger.info("✅ [Stream] 监听线程已正式启动（WebSocket 长连接模式，无需公网回调地址）")

    @classmethod
    def send_markdown_text_to_user(cls, content: str, user_id: str | None = None) -> bool:
        """
        向用户单聊发送 Markdown 格式的文本消息。
        适用于 AI 闲聊回复，支持加粗、列表等格式渲染。
        """
        logger.info(f"📝 [SendMarkdown] 准备发送 | User: {user_id or Config.USER_ID}")
        try:
            # 钉钉 sampleMarkdown 需要 title 和 text
            cls._send("sampleMarkdown", {"title": "AI 助理", "text": content}, user_id=user_id)
            return True
        except Exception as e:
            logger.error(f"❌ [SendMarkdown] 失败: {e}", exc_info=True)
            return False
