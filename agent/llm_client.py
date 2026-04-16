"""
ReportGenerator — LLM 日报润色引擎
新增：注入时间感知，修复盲目按 is_completed 分类的 Bug
"""
import json
from pathlib import Path
from openai import OpenAI

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("LLM_Client")

_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "report_polish_prompt.txt"


def build_summary_card(tasks: list) -> str:
    """提取摘要卡片构建逻辑供多处复用"""
    done = sum(1 for t in tasks if t["is_completed"])
    in_prog = sum(1 for t in tasks if not t["is_completed"] and t["progress"] > 0)
    planned = sum(1 for t in tasks if not t["is_completed"] and t["progress"] == 0)

    if not (done or in_prog or planned): return ""

    lines = ["| 任务状态 | 数量 |", "|:---:|:---:|"]
    if done: lines.append(f"| ✅ 已完成 | {done} |")
    if in_prog: lines.append(f"| ⏳ 推进中 | {in_prog} |")
    if planned: lines.append(f"| 📅 计划中 | {planned} |")
    return "\n".join(lines)


class ReportGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=Config.LLM_API_KEY,
            base_url=Config.LLM_BASE_URL,
        )
        self.model = Config.LLM_MODEL
        self._prompt_template = self._load_prompt()

    def _load_prompt(self) -> str:
        try:
            with open(_PROMPT_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _fmt_task(self, task: dict) -> str:
        if task["is_completed"]:
            tag = "[✅ 已完成]"
        elif task["progress"] > 0:
            tag = f"[⏳ 推进中 {task['bar']} {task['progress']}%]"
        else:
            tag = "[📅 计划中]"
        return f"{tag} {task['content']}"

    def generate(self, today_tasks: list[dict], tomorrow_tasks: list[dict]) -> dict:
        """核心修改：直接接收划分好日期的任务组"""
        today_str = "\n".join(self._fmt_task(t) for t in today_tasks) or "（无）"
        tomorrow_str = "\n".join(self._fmt_task(t) for t in tomorrow_tasks) or "（无）"

        if not self._prompt_template:
            return {"today_work": "生成失败", "tomorrow_plan": "生成失败"}

            # 核心修复：使用 replace 替代 format，防止与 prompt 中的 JSON 大括号冲突
        prompt = self._prompt_template.replace("{today_tasks}", today_str).replace("{tomorrow_tasks}", tomorrow_str)

        try:
            logger.info(f"调用大模型 {self.model} 生成日报...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                stream=False
            )
            raw = response.choices[0].message.content
            if raw is None: return {"today_work": "（未生成）", "tomorrow_plan": "（未生成）"}

            result = json.loads(raw)
            result.setdefault("today_work", "（未生成）")
            result.setdefault("tomorrow_plan", "（未生成）")
            return result
        except Exception as e:
            logger.error(f"大模型调用失败: {e}")
            return {"today_work": "生成失败", "tomorrow_plan": "生成失败"}
