"""
ReportGenerator — LLM 日报润色引擎
"""
import json
from pathlib import Path

from openai import OpenAI

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

    def _load_prompt(self) -> str:
        try:
            with open(_PROMPT_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _fmt_task(self, task: dict) -> str:
        if task["is_completed"]:
            tag = "[已完成]"
        elif task["progress"] > 0:
            tag = f"[推进中 {task['progress']}%]"
        else:
            tag = "[计划中]"
        return f"{tag} {task['content']}"

    def generate(self, today_tasks: list[dict], tomorrow_tasks: list[dict]) -> dict:
        """核心修改：直接接收划分好日期的任务组"""
        logger.info(f"[LLM.generate] 开始生成日报 | 今日任务={len(today_tasks)}条, 明日任务={len(tomorrow_tasks)}条")

        today_str = "\n".join(self._fmt_task(t) for t in today_tasks) or "（无）"
        tomorrow_str = "\n".join(self._fmt_task(t) for t in tomorrow_tasks) or "（无）"

        if not self._prompt_template:
            logger.error("❌ [LLM.generate] 提示词模板为空")
            return {"today_work": "生成失败", "tomorrow_plan": "生成失败"}

        # 核心修复：使用 replace 替代 format，防止与 prompt 中的 JSON 大括号冲突
        prompt = self._prompt_template.replace("{today_tasks}", today_str).replace("{tomorrow_tasks}", tomorrow_str)

        try:
            logger.info(f"🤖 [LLM.generate] 调用大模型 {self.model}...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                stream=False
            )

            logger.debug(f"[LLM.generate] 响应对象收到: choices数量={len(response.choices) if response.choices else 0}")

            if not response.choices:
                logger.error("❌ [LLM.generate] 响应中没有 choices")
                return {"today_work": "（未生成）", "tomorrow_plan": "（未生成）"}

            raw = response.choices[0].message.content
            logger.info(f"[LLM.generate] 原始响应长度: {len(raw) if raw else 0} 字符")
            logger.debug(f"[LLM.generate] 原始响应内容:\n{raw}")

            if raw is None:
                logger.warning("⚠️ [LLM.generate] 响应内容为 None")
                return {"today_work": "（未生成）", "tomorrow_plan": "（未生成）"}

            # 尝试解析 JSON
            try:
                result = json.loads(raw)
                logger.info(f"✅ [LLM.generate] JSON 解析成功")
                logger.info(f"   - today_work 长度: {len(result.get('today_work', ''))}")
                logger.info(f"   - tomorrow_plan 长度: {len(result.get('tomorrow_plan', ''))}")
            except json.JSONDecodeError as je:
                logger.error(f"❌ [LLM.generate] JSON 解析失败: {je}")
                logger.error(f"原始内容前500字符: {raw[:500]}")
                # 尝试提取 JSON 部分
                import re
                json_match = re.search(r'\{.*\}', raw, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                        logger.warning("⚠️ [LLM.generate] 从响应中提取到 JSON 片段")
                    except:
                        result = {"today_work": "JSON解析失败", "tomorrow_plan": raw[:200]}
                else:
                    result = {"today_work": "JSON解析失败", "tomorrow_plan": raw[:200]}

            result.setdefault("today_work", "（未生成）")
            result.setdefault("tomorrow_plan", "（未生成）")

            logger.info(f"✅ [LLM.generate] 日报生成完成")
            return result

        except Exception as e:
            logger.error(f"❌ [LLM.generate] 调用异常: {e}", exc_info=True)
            return {"today_work": "生成失败", "tomorrow_plan": "生成失败"}
