"""
ReportGenerator — LLM 日报润色引擎
"""
import json
import time
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
        start_time = time.time()
        logger.info(f"[LLM.generate] 开始生成日报 | 今日任务={len(today_tasks)}条, 明日任务={len(tomorrow_tasks)}条")

        today_str = "\n".join(self._fmt_task(t) for t in today_tasks) or "（无）"
        tomorrow_str = "\n".join(self._fmt_task(t) for t in tomorrow_tasks) or "（无）"
        
        logger.debug(f"[LLM.generate] 提示词长度: 今日={len(today_str)}字符, 明日={len(tomorrow_str)}字符")

        if not self._prompt_template:
            logger.error("❌ [LLM.generate] 提示词模板为空")
            return {"today_work": "生成失败", "tomorrow_plan": "生成失败"}

        # 核心修复：使用 replace 替代 format，防止与 prompt 中的 JSON 大括号冲突
        prompt = self._prompt_template.replace("{today_tasks}", today_str).replace("{tomorrow_tasks}", tomorrow_str)
        logger.debug(f"[LLM.generate] 完整提示词长度: {len(prompt)}字符")

        try:
            logger.info(f"🤖 [LLM.generate] 调用大模型 {self.model}...")
            api_start = time.time()

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                # 移除 response_format，因为我们现在使用固定文本格式而非 JSON
                stream=False
            )
            
            api_elapsed = time.time() - api_start
            logger.info(f"⏱️ [LLM.generate] API 调用耗时: {api_elapsed:.2f}秒")

            logger.debug(f"[LLM.generate] 响应对象收到: choices数量={len(response.choices) if response.choices else 0}")

            if not response.choices:
                logger.error("❌ [LLM.generate] 响应中没有 choices")
                return {"today_work": "（未生成）", "tomorrow_plan": "（未生成）"}

            raw = response.choices[0].message.content
            logger.info(f"[LLM.generate] 原始响应长度: {len(raw) if raw else 0} 字符")
            logger.info(f"[LLM.generate] 原始响应内容:\n{raw}")

            if raw is None:
                logger.warning("⚠️ [LLM.generate] 响应内容为 None")
                return {"today_work": "（未生成）", "tomorrow_plan": "（未生成）"}

            # 解析固定格式文本
            try:
                # 查找分隔符
                today_marker = "===TODAY==="
                tomorrow_marker = "===TOMORROW==="
                
                today_start = raw.find(today_marker)
                tomorrow_start = raw.find(tomorrow_marker)
                
                if today_start == -1 or tomorrow_start == -1:
                    logger.warning("⚠️ [LLM.generate] 未找到分隔符，尝试直接返回")
                    result = {"today_work": raw.strip(), "tomorrow_plan": "（未生成）"}
                else:
                    # 提取今日工作（从 ===TODAY=== 到 ===TOMORROW===）
                    today_work = raw[today_start + len(today_marker):tomorrow_start].strip()
                    # 提取明日计划（从 ===TOMORROW=== 到结尾）
                    tomorrow_plan = raw[tomorrow_start + len(tomorrow_marker):].strip()
                    
                    result = {
                        "today_work": today_work if today_work else "（未生成）",
                        "tomorrow_plan": tomorrow_plan if tomorrow_plan else "（未生成）"
                    }
                
                logger.info(f"✅ [LLM.generate] 文本解析成功")
                logger.info(f"   - today_work 长度: {len(result.get('today_work', ''))}")
                logger.info(f"   - tomorrow_plan 长度: {len(result.get('tomorrow_plan', ''))}")
                
            except Exception as pe:
                logger.error(f"❌ [LLM.generate] 文本解析失败: {pe}")
                logger.error(f"原始内容前500字符: {raw[:500]}")
                result = {"today_work": "解析失败", "tomorrow_plan": raw[:200]}

            result.setdefault("today_work", "（未生成）")
            result.setdefault("tomorrow_plan", "（未生成）")

            total_elapsed = time.time() - start_time
            logger.info(f"✅ [LLM.generate] 日报生成完成 | 总耗时: {total_elapsed:.2f}秒")
            return result

        except Exception as e:
            logger.error(f"❌ [LLM.generate] 调用异常: {e}", exc_info=True)
            return {"today_work": "生成失败", "tomorrow_plan": "生成失败"}
