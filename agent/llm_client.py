import os
import json

from openai import OpenAI

from common.logger import get_logger

logger = get_logger("LLM_Client")


class ReportGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL")
        )
        self.model = os.getenv("LLM_MODEL")
        self.prompt_template = self._load_prompt_template()

    def _load_prompt_template(self):
        """Loads the prompt template from a file."""
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "report_polish_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {prompt_path}")
            return ""

    def _format_task_for_prompt(self, task):
        """将单个任务格式化为带状态和进度条的字符串"""
        if task['is_completed']:
            status = "[✅ 已完成]"
        elif task['progress'] > 0:
            status = f"[⏳ 推进中 {task['bar']} {task['progress']}%]"
        else:
            status = "[📅 计划中]"
        
        return f"{status} {task['content']}"

    def generate(self, tasks: list) -> dict:
        """
        接收解析好的任务列表，返回润色后的今日工作、明日计划和总结卡片
        """
        today_tasks = [t for t in tasks if t['is_completed']]
        tomorrow_tasks = [t for t in tasks if not t['is_completed']]

        today_tasks_str = "\\n".join(self._format_task_for_prompt(t) for t in today_tasks) or "无"
        tomorrow_tasks_str = "\\n".join(self._format_task_for_prompt(t) for t in tomorrow_tasks) or "无"

        if not self.prompt_template:
            logger.error("Prompt template not loaded. Cannot generate report.")
            return {"today_work": "生成失败", "tomorrow_plan": "生成失败", "summary_card": ""}

        prompt = self.prompt_template.format(
            today_tasks=today_tasks_str,
            tomorrow_tasks=tomorrow_tasks_str
        )

        try:
            logger.info("正在调用大模型生成日报内容...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            result = response.choices[0].message.content
            # 确保返回的 JSON 包含所有期望的键
            report_data = json.loads(result)
            report_data.setdefault("today_work", "")
            report_data.setdefault("tomorrow_plan", "")
            report_data.setdefault("summary_card", "")
            return report_data
        except Exception as e:
            logger.error(f"大模型调用失败: {e}")
            return {"today_work": "生成失败", "tomorrow_plan": "生成失败", "summary_card": ""}
