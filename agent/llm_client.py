"""
ReportGenerator — LLM 润色引擎（需求 6）
接收 TodoParser 输出 → 调用大模型 → 返回结构化日报字典
"""
import json
from pathlib import Path
from typing import cast

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionUserMessageParam

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("LLM_Client")

_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "report_polish_prompt.txt"


class ReportGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=Config.LLM_API_KEY,
            base_url=Config.LLM_BASE_URL,
        )
        self.model = Config.LLM_MODEL
        self._prompt_template = self._load_prompt()

    # ── 内部工具 ──────────────────────────────────────────────

    def _load_prompt(self) -> str:
        try:
            with open(_PROMPT_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Prompt 模板文件不存在: {_PROMPT_PATH}")
            return ""

    def _fmt_task(self, task: dict) -> str:
        """将任务对象格式化为给 LLM 的单行描述"""
        if task["is_completed"]:
            tag = "[✅ 已完成]"
        elif task["progress"] > 0:
            tag = f"[⏳ 推进中 {task['bar']} {task['progress']}%]"
        else:
            tag = "[📅 计划中]"
        return f"{tag} {task['content']}"

    # ── 公开接口 ──────────────────────────────────────────────

    def generate(self, tasks: list[dict]) -> dict:
        """
        接收解析好的任务列表，返回润色后的日报字典：
        {today_work, tomorrow_plan, summary_card}
        """
        today_tasks = [t for t in tasks if t["is_completed"]]
        tomorrow_tasks = [t for t in tasks if not t["is_completed"]]

        today_str = "\n".join(self._fmt_task(t) for t in today_tasks) or "（无）"
        tomorrow_str = "\n".join(self._fmt_task(t) for t in tomorrow_tasks) or "（无）"

        if not self._prompt_template:
            logger.error("Prompt 模板为空，无法生成日报")
            return {"today_work": "生成失败", "tomorrow_plan": "生成失败", "summary_card": ""}

        prompt = self._prompt_template.format(
            today_tasks=today_str,
            tomorrow_tasks=tomorrow_str,
        )

        try:
            logger.info(f"调用大模型 {self.model} 生成日报...")
            message: ChatCompletionUserMessageParam = {
                "role": "user",
                "content": prompt
            }
            response = cast(
                ChatCompletion,
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[message],
                    response_format={"type": "json_object"},  # type: ignore
                ),
            )
            raw = response.choices[0].message.content
            if raw is None:
                logger.warning("大模型返回内容为空")
                return {"today_work": "生成失败", "tomorrow_plan": "生成失败", "summary_card": ""}

            result = json.loads(raw)
            result.setdefault("today_work", "（未生成）")
            result.setdefault("tomorrow_plan", "（未生成）")
            result.setdefault("summary_card", "")
            logger.info("✅ 大模型日报生成完成")
            return result
        except Exception as e:
            logger.error(f"大模型调用失败: {e}")
            return {"today_work": "生成失败", "tomorrow_plan": "生成失败", "summary_card": ""}
