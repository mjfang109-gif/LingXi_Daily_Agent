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
        # 初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=Config.LLM_API_KEY,
            base_url=Config.LLM_BASE_URL,
        )
        # 加载模型名称配置
        self.model = Config.LLM_MODEL

        # 获取用户位置信息
        location = Config.get("llm.location", "")

        # 获取位置上下文提示词模板
        location_prompt_template = Config.get(
            "llm.location_prompt",
            "你已了解用户位于「{location}」，当用户询问天气、出行、本地资讯等相关问题时，可以结合该位置给出更准确的回答。"
        )

        # 获取联网搜索配置
        # 支持格式：
        # - provider: "qwen" / "deepseek" / "moonshot" / "zhipu" / "custom"
        # - extra_body: 自定义参数（仅 custom 时使用）
        self._web_search_config = Config.get("llm.web_search", {"provider": "qwen"})

        # 构建 System Prompt
        system_prompt_template = Config.get(
            "llm.chat_system_prompt",
            "你是一个全能办公助理，请简短回答用户的问题，并在结尾提醒用户可以通过特定格式发送工作任务。"
        )

        # 追加位置上下文（如果有配置）
        if location and location_prompt_template:
            location_context = f"\n\n【用户位置信息】\n{location_prompt_template.format(location=location)}"
            self._system_prompt = system_prompt_template + location_context
            logger.info(f"已加载用户位置配置: {location}")
        else:
            self._system_prompt = system_prompt_template

        logger.info(f"AIChatEngine 初始化完成，使用模型: {self.model}, 联网搜索: {self._web_search_config}")

    def chat(self, user_msg: str) -> str:
        """
        执行对话交互并返回结果
        
        Args:
            user_msg (str): 用户输入的消息内容
            
        Returns:
            str: AI 生成的回复内容或错误提示信息
        """
        try:
            logger.info(f"开始处理用户自由对话请求，模型: {self.model}")
            logger.debug(f"用户输入内容: {user_msg}")
            logger.debug(f"System Prompt: {self._system_prompt}")

            # 核心修复：智能判断是否需要联网搜索
            extra_body = {}
            if self._web_search_config:
                provider = ""
                if isinstance(self._web_search_config, dict):
                    provider = self._web_search_config.get("provider", "")
                else:
                    # backwards compatibility: 旧版 boolean 配置
                    if self._web_search_config is True:
                        provider = "qwen"

                # 定义需要联网的场景关键词
                user_msg_lower = user_msg.lower()
                search_keywords = [
                    '天气', '新闻', '资讯', '查询', '搜索', '最新', '实时',
                    '股票', '汇率', '比分', '排名', '价格', '路线',
                    'weather', 'news', 'search', 'latest', 'stock'
                ]
                
                # 检查用户输入是否包含搜索关键词
                need_search = any(keyword in user_msg_lower for keyword in search_keywords)
                
                if need_search:
                    if provider == "qwen":
                        extra_body = {"enable_search": True}
                        logger.info("启用阿里千问联网搜索")
                    elif provider == "deepseek":
                        extra_body = {"enable_search": True}
                        logger.info("启用 DeepSeek 联网搜索")
                    elif provider == "moonshot":
                        extra_body = {"search_options": {"enable": True}}
                        logger.info("启用 Moonshot 月之暗面联网搜索")
                    elif provider == "zhipu":
                        extra_body = {"search_retrieval": True}
                        logger.info("启用智谱 GLM 联网搜索")
                    elif provider == "custom":
                        extra_body = self._web_search_config.get("extra_body", {})
                        logger.info(f"启用自定义联网搜索: {extra_body}")
                    else:
                        if provider:
                            logger.warning(f"未知的 provider '{provider}'，默认使用千问联网参数")
                        extra_body = {"enable_search": True}
                        logger.info("启用联网搜索（默认千问）")
                else:
                    logger.debug("无需联网搜索，直接使用模型生成")

            # 构建调用参数
            call_kwargs = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self._system_prompt},
                    {"role": "user", "content": user_msg}
                ],
                "temperature": 0.7,
                "stream": False,
            }

            if extra_body:
                call_kwargs["extra_body"] = extra_body

            # 调用大模型 API 生成回复
            response = self.client.chat.completions.create(**call_kwargs)

            # 提取回复内容
            reply = response.choices[0].message.content
            logger.info(f"大模型回复成功，内容长度: {len(reply) if reply else 0}")
            logger.debug(f"大模型原始回复: {reply}")

            # 若回复为空，返回默认兜底提示
            if not reply:
                logger.warning("大模型返回空内容，使用默认兜底回复")
                return "抱歉，我现在脑子有点短路，无法回答。记得如果写日报，请用格式「1. 任务@日期」发给我哦~"

            return reply

        except Exception as e:
            # 记录详细错误日志
            logger.error(f"AI 聊天接口调用失败: {e}", exc_info=True)
            return "糟糕，我的 AI 语言中枢似乎断开了连接... 请稍后再试。如果你是来记录日报的，请直接按格式发送给我。"
