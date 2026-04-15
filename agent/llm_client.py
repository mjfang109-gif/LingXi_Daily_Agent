import os

from openai import OpenAI

from common.logger import get_logger

logger = get_logger("LLM_Client")


class ReportGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL")
        )
        self.model = os.getenv("LLM_MODEL")  # 可在 .env 中自定义模型

    def generate(self, tasks: list) -> dict:
        """
        接收解析好的任务列表，返回润色后的今日工作和明日计划
        tasks 格式: [{"content": "...", "date": "4.15", "is_completed": True}, ...]
        """
        today_tasks = [t['content'] for t in tasks if t['is_completed']]
        tomorrow_tasks = [t['content'] for t in tasks if not t['is_completed']]

        prompt = f"""
        你是一位高级职场助理，请根据以下极其简短的工作备忘，帮我扩写成一份正式、专业的工作日报。
        请将口语化的词汇转换为专业的职场术语。

        【今日已完成原始记录】：
        {chr(10).join(today_tasks) if today_tasks else "无"}

        【明日计划原始记录】：
        {chr(10).join(tomorrow_tasks) if tomorrow_tasks else "无"}

        请严格按以下 JSON 格式返回，不要输出多余废话：
        {{
            "today_work": "1. 专业化润色后的第一条\\n2. 专业化润色后的第二条",
            "tomorrow_plan": "1. 专业化润色后的第一条\\n2. 专业化润色后的第二条"
        }}
        """

        try:
            logger.info("正在调用大模型生成日报内容...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}  # 强制返回 JSON
            )
            result = response.choices[0].message.content
            import json
            return json.loads(result)
        except Exception as e:
            logger.error(f"大模型调用失败: {e}")
            return {"today_work": "生成失败", "tomorrow_plan": "生成失败"}