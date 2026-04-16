"""
AIChatEngine — 开放对话与智能助理引擎
职责：专门处理用户非规范任务的自由对话，并从 config.yaml 读取 System Prompt
"""
from openai import OpenAI

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("Chat_Engine")


class AIChatEngine:
    """处理用户闲聊与通用提问的全能 AI 引擎"""

    def __init__(self):
        self.client = OpenAI(
            api_key=Config.LLM_API_KEY,
            base_url=Config.LLM_BASE_URL,
        )
        self.model = Config.LLM_MODEL
        # 从配置文件加载 prompt，并提供兜底的默认值防止配置缺失
        self._system_prompt = Config.get(
            "llm.chat_system_prompt",
            "你是一个全能办公助理，请简短回答用户的问题，并在结尾提醒用户可以通过特定格式发送工作任务。"
        )

    def chat(self, user_msg: str) -> str:
        """执行对话交互并返回结果"""
        try:
            logger.info(f"调用大模型 {self.model} 处理用户自由对话...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[  # type: ignore[arg-type]
                    {"role": "system", "content": self._system_prompt},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.7,
                stream=False,
            )
            reply = response.choices[0].message.content
            return reply or "抱歉，我现在脑子有点短路，无法回答。记得如果写日报，请用格式「1. 任务@日期」发给我哦~"

        except Exception as e:
            logger.error(f"AI 聊天接口调用失败: {e}")
            return "糟糕，我的 AI 语言中枢似乎断开了连接... 请稍后再试。如果你是来记录日报的，请直接按格式发送给我。"
