"""
Agent 主程序
钉钉消息 → LLM Tool-Use 循环 → ReplyMessage → 钉钉回复（text / markdown卡片）
"""

import asyncio
import logging
import sys
import dingtalk_stream
from dingtalk_stream import ChatbotHandler, AckMessage, ChatbotMessage
from datetime import datetime

from config import Config
from llm import LLMFactory
from llm.base import ReplyMessage
from business import BusinessRouter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


class DataQueryHandler(ChatbotHandler):
    """钉钉消息处理器 - 支持 text 和 markdown 卡片回复"""

    def __init__(self, llm, router: BusinessRouter):
        super().__init__()
        self.llm = llm
        self.llm.register_tool_handlers(router.get_tool_handlers())

    async def process(self, callback):
        start = datetime.now()
        incoming_message = None

        try:
            incoming_message = ChatbotMessage.from_dict(callback.data)
            user_id = incoming_message.sender_staff_id
            user_message = incoming_message.text.content.strip()

            logger.info("=" * 70)
            logger.info(f"📨 用户: {user_id}")
            logger.info(f"📝 消息: {user_message}")

            # LLM 处理（含 Tool-Use 循环）
            reply: ReplyMessage = await self.llm.run(user_message)

            elapsed = (datetime.now() - start).total_seconds()
            logger.info(f"✅ 完成 | 耗时: {elapsed:.2f}s | 格式: {reply.format}")

            # 根据 format 选择钉钉回复方式
            self._send_reply(reply, incoming_message)
            return AckMessage.STATUS_OK, "OK"

        except Exception as e:
            elapsed = (datetime.now() - start).total_seconds()
            logger.error(f"❌ 异常 | 耗时: {elapsed:.2f}s | {e}", exc_info=True)
            try:
                if incoming_message:
                    self.reply_text("处理您的问题时出现了点问题，请稍后重试。", incoming_message)
            except Exception:
                pass
            return AckMessage.STATUS_INTERNAL_ERROR, str(e)

    def _send_reply(self, reply: ReplyMessage, incoming_message: ChatbotMessage):
        """根据 format 发送对应格式的钉钉消息"""
        if reply.is_markdown:
            try:
                self.reply_markdown(
                    title=reply.title or "查询结果",
                    text=reply.content,
                    incoming_message=incoming_message
                )
                logger.info(f"📊 Markdown卡片已发送: {reply.title}")
                return
            except Exception as e:
                # Markdown 发送失败时降级为纯文本
                logger.warning(f"Markdown 卡片发送失败，降级为纯文本: {e}")
                fallback = self._md_to_plain(reply.content)
                self.reply_text(f"【{reply.title}】\n\n{fallback}", incoming_message)
        else:
            self.reply_text(reply.content, incoming_message)
            logger.info("💬 纯文字已发送")

    @staticmethod
    def _md_to_plain(text: str) -> str:
        """Markdown 降级为纯文本（应急用）"""
        import re
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
        text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*-\s+', '  ', text, flags=re.MULTILINE)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


async def main():
    logger.info("=" * 60)
    logger.info("客户管理 Agent 启动")
    logger.info("=" * 60)

    if not Config.DINGTALK_CLIENT_ID or not Config.DINGTALK_CLIENT_SECRET:
        logger.error("❌ 钉钉凭证未配置，请在 .env 中设置")
        return
    if not Config.LLM_API_KEY:
        logger.error("❌ 大模型 API Key 未配置，请在 .env 中设置 LLM_API_KEY")
        return

    try:
        llm = LLMFactory.create(
            provider=Config.LLM_PROVIDER,
            api_key=Config.LLM_API_KEY,
            model=Config.LLM_MODEL,
            base_url=Config.LLM_BASE_URL,
            enable_search=Config.ENABLE_WEB_SEARCH,
        )
        logger.info(f"✅ 大模型: {Config.LLM_PROVIDER}/{Config.LLM_MODEL}")
    except Exception as e:
        logger.error(f"❌ 大模型初始化失败: {e}")
        return

    try:
        router = BusinessRouter(Config)
        logger.info(f"✅ 业务系统: {Config.BUSINESS_BASE_URL}")
    except Exception as e:
        logger.error(f"❌ 业务系统初始化失败: {e}")
        return

    credential = dingtalk_stream.Credential(
        client_id=Config.DINGTALK_CLIENT_ID,
        client_secret=Config.DINGTALK_CLIENT_SECRET,
    )
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_callback_handler(
        dingtalk_stream.chatbot.ChatbotMessage.TOPIC,
        DataQueryHandler(llm, router)
    )

    logger.info("=" * 60)
    logger.info("✅ Agent 已就绪，等待钉钉消息...")
    logger.info("=" * 60)

    try:
        await client.start()
    except KeyboardInterrupt:
        logger.info("\n👋 Agent 已停止")
    except Exception as e:
        logger.error(f"❌ 运行异常: {e}", exc_info=True)
    finally:
        await router.close()


if __name__ == "__main__":
    asyncio.run(main())
