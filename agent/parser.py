"""
TodoParser — 任务解析器
支持格式：序号. 任务描述@日期@状态（进度XX%）

示例：
  1. 修复登录Bug@4.15
  2. 梳理架构@4.16@未完成
  3. 性能优化@4.17，进度60%
"""
import re
from datetime import datetime

from common.logger import get_logger

logger = get_logger("Parser")

# 统一格式正则：序号. 内容 [，进度N%] [@日期] [@状态]
_PATTERN = re.compile(
    r"^\d+[\.、]\s*"  # 序号（兼容 . 和 、）
    r"(?P<content>[^@，,]+?)"  # 任务描述（必填）
    r"(?:[，,]进度(?P<progress>\d+)%)?"  # 进度（可选）
    r"(?:@(?P<date>[\d\./\-]+))?"  # 日期（可选）
    r"(?:@(?P<status>已完成|未完成))?$"  # 状态（可选）
)

_BAR_LENGTH = 10


def _build_bar(percent: int) -> str:
    """生成文本进度条 ▓▓▓░░ 格式（需求 8）"""
    filled = round(_BAR_LENGTH * percent / 100)
    return "▓" * filled + "░" * (_BAR_LENGTH - filled)


def _normalize_date(raw: str) -> str:
    """将 4.15 / 4-15 / 2025-04-15 统一为 MM-DD 可读字符串"""
    if not raw:
        return datetime.now().strftime("%m-%d")
    raw = raw.strip().replace("/", "-").replace(".", "-")
    parts = raw.split("-")
    if len(parts) == 2:
        return f"{int(parts[0]):02d}-{int(parts[1]):02d}"
    if len(parts) == 3:
        return f"{int(parts[1]):02d}-{int(parts[2]):02d}"
    return raw


class TodoParser:
    @classmethod
    def parse_file(cls, file_path: str) -> list[dict]:
        """解析 todo.md，返回任务列表"""
        tasks = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            logger.error(f"任务文件不存在: {file_path}")
            return tasks
        except Exception as e:
            logger.error(f"读取任务文件异常: {e}")
            return tasks

        today_str = datetime.now().strftime("%m-%d")

        for line in lines:
            line = line.strip()
            if not line:
                continue
            m = _PATTERN.match(line)
            if not m:
                logger.debug(f"跳过非任务行: {line!r}")
                continue

            content = m.group("content").strip()
            raw_prog = m.group("progress")
            raw_date = m.group("date")
            raw_stat = m.group("status")

            # 状态字段可选，默认视为已完成（需求 2）
            is_completed = raw_stat != "未完成"

            # 日期字段可选，未写日期默认归入今日（需求 2）
            date_str = _normalize_date(raw_date) if raw_date else today_str

            # 进度推断：已完成=100，未完成且无进度=0
            if raw_prog is not None:
                progress = int(raw_prog)
            else:
                progress = 100 if is_completed else 0

            tasks.append({
                "content": content,
                "progress": progress,
                "bar": _build_bar(progress),
                "date": date_str,
                "is_completed": is_completed,
            })

        logger.info(f"共解析到 {len(tasks)} 条任务")
        return tasks
