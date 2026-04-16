"""
TodoParser — 任务解析器
新增：严格的 YYYY-MM-DD 日期归一化机制
"""
import re
from datetime import datetime

from common.logger import get_logger

logger = get_logger("Parser")

_PATTERN = re.compile(
    r"^\d+[\.、]\s*"
    r"(?P<content>[^@，,\n]+?)"
    r"(?:[，,]\s*进度(?P<progress>\d+)%)?"
    r"(?:@(?P<date>[\d\./\-]+))?"
    r"(?:@(?P<status>已完成|未完成))?"
    r"\s*$"
)

_TASK_LINE_HINT = re.compile(r"^\s*\d+[\.、]\s*\S")
_BAR_LENGTH = 10


def _build_bar(percent: int) -> str:
    filled = round(_BAR_LENGTH * percent / 100)
    return "▓" * filled + "░" * (_BAR_LENGTH - filled)


def _normalize_date(raw: str, now_dt: datetime) -> str:
    """将 4.15 / 4-15 统一归一化为标准的 YYYY-MM-DD，解决时间比较 Bug"""
    if not raw:
        return now_dt.strftime("%Y-%m-%d")

    raw = raw.strip().replace("/", "-").replace(".", "-")
    parts = raw.split("-")
    try:
        if len(parts) == 2:
            month, day = int(parts[0]), int(parts[1])
            # 处理跨年逻辑：如果当前是12月，写的日期是1月，认为是明年
            year = now_dt.year + 1 if now_dt.month == 12 and month == 1 else now_dt.year
            return f"{year}-{month:02d}-{day:02d}"
        if len(parts) == 3:
            year = int(parts[0])
            if year < 100: year += 2000
            return f"{year}-{int(parts[1]):02d}-{int(parts[2]):02d}"
    except (ValueError, IndexError):
        pass
    return now_dt.strftime("%Y-%m-%d")


def _parse_line(line: str, now_dt: datetime) -> dict | None:
    line = line.strip()
    if not line: return None

    m = _PATTERN.match(line)
    if not m: return None

    content = m.group("content").strip()
    raw_prog = m.group("progress")
    raw_date = m.group("date")
    raw_stat = m.group("status")

    is_completed = raw_stat != "未完成"
    date_str = _normalize_date(raw_date, now_dt)

    if raw_prog is not None:
        progress = int(raw_prog)
    else:
        progress = 100 if is_completed else 0

    return {
        "content": content,
        "progress": progress,
        "bar": _build_bar(progress),
        "date": date_str,
        "is_completed": is_completed,
    }


class TodoParser:
    @staticmethod
    def is_task_message(text: str) -> bool:
        if not text or not text.strip(): return False
        stripped = text.strip().upper()
        if stripped in ("Y", "N", "YES", "NO", "是", "否", "确认", "取消"):
            return False

        lines = [ln for ln in text.splitlines() if ln.strip()]
        if not lines: return False

        task_lines = sum(1 for ln in lines if _TASK_LINE_HINT.match(ln))
        return task_lines >= 1 and task_lines / len(lines) > 0.5

    @classmethod
    def parse_message(cls, text: str) -> list[dict]:
        if not text: return []

        now_dt = datetime.now()
        tasks = []
        for line in text.splitlines():
            task = _parse_line(line, now_dt)
            if task:
                tasks.append(task)

        logger.info(f"从消息解析到 {len(tasks)} 条任务")
        return tasks
