"""
TodoParser — 任务解析器
支持：单日期、日期范围（如 4.17-4.21）
"""
import json
import os
import re
from datetime import datetime, timedelta

from common.logger import get_logger

logger = get_logger("Parser")

# 支持单日期和日期范围（如 4.17, 4.17-4.21, 2026-04-17-2026-04-21）
# 注意：content 中允许包含逗号，通过 @ 符号来分隔内容和日期
# 增强容错：支持 @4.17-4.22、@4.17-@4.22、4.17-4.22 等多种格式
_PATTERN = re.compile(
    r"^\d+[\.、]\s*"
    r"(?P<content>.+?)"  # 允许内容中包含逗号
    r"(?:[，,]\s*进度(?P<progress>\d+)%)?"  # 可选的进度信息
    r"(?:@?(?P<date>[\d\./\-]+(?:-@?[\d\./\-]+)?))?"  # 可选的日期或日期范围，@ 可选，容忍多余的 @
    r"(?:@(?P<status>已完成|未完成))?"  # 可选的状态
    r"\s*$"
)

_TASK_LINE_HINT = re.compile(r"^\s*\d+[\.、]\s*\S")
_BAR_LENGTH = 10


def _normalize_date(raw: str, now_dt: datetime) -> str:
    """
    将非标准日期字符串归一化为 YYYY-MM-DD 格式。
    支持格式: MM.DD, MM-DD, YYYY.MM.DD, YYYY-MM-DD 等。

    Args:
        raw (str): 原始日期字符串，可能为空。
        now_dt (datetime): 当前时间对象，用于推断年份。

    Returns:
        str: 标准化后的日期字符串 (YYYY-MM-DD)。
    """
    logger.debug(f"[_normalize_date] 入参: raw='{raw}', now_dt={now_dt}")

    if not raw:
        default_date = now_dt.strftime("%Y-%m-%d")
        logger.debug(f"[_normalize_date] raw 为空，返回默认日期: {default_date}")
        return default_date

    # 统一分隔符为 '-'
    normalized_raw = raw.strip().replace("/", "-").replace(".", "-")
    parts = normalized_raw.split("-")

    result_date = now_dt.strftime("%Y-%m-%d")

    try:
        if len(parts) == 2:
            # 处理 MM-DD 格式
            month, day = int(parts[0]), int(parts[1])
            # 处理跨年逻辑：如果当前是12月，写的日期是1月，认为是明年
            year = now_dt.year + 1 if now_dt.month == 12 and month == 1 else now_dt.year
            result_date = f"{year}-{month:02d}-{day:02d}"
            logger.debug(f"[_normalize_date] 解析 MM-DD: '{raw}' -> '{result_date}'")

        elif len(parts) == 3:
            # 处理 YYYY-MM-DD 或 YY-MM-DD 格式
            year = int(parts[0])
            if year < 100:
                year += 2000
            result_date = f"{year}-{int(parts[1]):02d}-{int(parts[2]):02d}"
            logger.debug(f"[_normalize_date] 解析 YYYY-MM-DD: '{raw}' -> '{result_date}'")
        else:
            logger.warning(f"[_normalize_date] 日期格式部分数量异常 ({len(parts)}): '{raw}'，使用默认日期")

    except (ValueError, IndexError) as e:
        logger.warning(f"[_normalize_date] 日期解析失败: '{raw}', 错误: {e}，使用默认日期")

    logger.debug(f"[_normalize_date] 出参: date='{result_date}'")
    return result_date


def _parse_date_range(raw: str, now_dt: datetime) -> list[str]:
    """
    解析日期范围，返回日期列表。
    支持格式：4.17-4.21, @4.17-4.21, @4.17-@4.21, 04-17-04-21, 2026-04-17-2026-04-21 等。

    Args:
        raw (str): 原始日期范围字符串（如 "4.17-4.21"）
        now_dt (datetime): 当前时间对象

    Returns:
        list[str]: 日期字符串列表 (YYYY-MM-DD 格式)
    """
    if not raw or "-" not in raw:
        return [_normalize_date(raw, now_dt)]

    # 统一分隔符，并移除多余的 @ 符号（容错处理）
    normalized = raw.strip().replace("/", "-").replace(".", "-").replace("@", "")

    # 尝试两种分割方式：按 - 分割成 2 或 4 个部分
    parts = normalized.split("-")

    try:
        # 情况1: MM-DD-MM-DD (如 4.17-4.21 -> ["4", "17", "4", "21"])
        if len(parts) == 4:
            start_month, start_day = int(parts[0]), int(parts[1])
            end_month, end_day = int(parts[2]), int(parts[3])

            # 处理跨年
            start_year = now_dt.year
            if now_dt.month == 12 and start_month == 1:
                start_year = now_dt.year + 1
            # 结束年份：如果开始月是12，结束月是1，认为是明年
            end_year = start_year + 1 if start_month == 12 and end_month == 1 else start_year

            dates = []
            current = datetime(start_year, start_month, start_day)
            end = datetime(end_year, end_month, end_day)

            while current <= end:
                dates.append(current.strftime("%Y-%m-%d"))
                current += timedelta(days=1)

            logger.debug(f"[_parse_date_range] 解析日期范围 MM-DD-MM-DD: '{raw}' -> {dates}")
            return dates

        # 情况2: YYYYMMDD-YYMMDD 或 YYYY-MM-DD-YYYY-MM-DD
        elif len(parts) == 6:
            # 格式: 2026-04-17-2026-04-21
            start_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
            end_date = f"{parts[3]}-{parts[4]}-{parts[5]}"

            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")

            dates = []
            current = start_dt
            while current <= end_dt:
                dates.append(current.strftime("%Y-%m-%d"))
                current += timedelta(days=1)

            logger.debug(f"[_parse_date_range] 解析日期范围 YYYY-MM-DD: '{raw}' -> {dates}")
            return dates

    except (ValueError, IndexError) as e:
        logger.warning(f"[_parse_date_range] 日期范围解析失败: '{raw}', 错误: {e}")

    # 解析失败，尝试作为单日期处理
    return [_normalize_date(raw, now_dt)]


# 全局节假日缓存（已废弃，统一使用 LocalFileService）
# 保留此代码仅为向后兼容，新代码应使用 mcp_server.services.local_fs.LocalFileService
_HOLIDAY_CACHE = {}
# 使用项目根目录的 holiday.json
_HOLIDAY_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "holiday.json")


def _load_holidays_local():
    global _HOLIDAY_CACHE
    if not _HOLIDAY_CACHE:
        try:
            if os.path.exists(_HOLIDAY_FILE_PATH):
                with open(_HOLIDAY_FILE_PATH, 'r', encoding='utf-8') as f:
                    _HOLIDAY_CACHE = json.load(f)
                logger.info(f"✅ 本地节假日配置加载成功，共 {len(_HOLIDAY_CACHE)} 条记录")
            else:
                logger.warning("⚠️ holiday.json 文件不存在，将默认所有日期为工作日")
        except Exception as e:
            logger.error(f"❌ 加载 holiday.json 失败: {e}")


def _is_workday_local(date_str: str) -> bool:
    """
    基于本地缓存判断是否为工作日
    
    注意：此函数已废弃，请使用 mcp_server.services.local_fs.LocalFileService.is_holiday()
    保留此函数仅为向后兼容
    """
    _load_holidays_local()

    # 1. 检查是否在节假日配置中
    if date_str in _HOLIDAY_CACHE:
        info = _HOLIDAY_CACHE[date_str]
        # isOffDay: true 表示休息，false 表示调休上班
        return not info.get("isOffDay", False)

    # 2. 不在配置中，检查是否为周末
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.weekday() < 5  # 0-4 为工作日
    except Exception:
        return True


def _parse_line(line: str, now_dt: datetime) -> list[dict]:
    """
    解析单行任务文本，支持日期范围。

    Args:
        line (str): 原始任务行文本。
        now_dt (datetime): 当前时间对象，用于日期归一化。

    Returns:
        list[dict]: 解析后的任务字典列表（支持日期范围拆分）
    """
    logger.debug(f"[_parse_line] 入参: line='{line}', now_dt={now_dt}")

    line = line.strip()
    if not line:
        logger.debug(f"[_parse_line] 空行，跳过")
        return []

    m = _PATTERN.match(line)
    if not m:
        logger.debug(f"[_parse_line] 正则匹配失败: '{line}'")
        return []

    content = m.group("content").strip()
    raw_prog = m.group("progress")
    raw_date = m.group("date")
    raw_stat = m.group("status")

    logger.debug(
        f"[_parse_line] 正则捕获组: content='{content}', progress={raw_prog}, date={raw_date}, status={raw_stat}")

    is_completed = raw_stat != "未完成"

    # 解析日期或日期范围
    date_list = _parse_date_range(raw_date, now_dt) if raw_date else [now_dt.strftime("%Y-%m-%d")]

    if raw_prog is not None:
        try:
            base_progress = int(raw_prog)
        except ValueError:
            logger.warning(f"[_parse_line] 进度值非法: '{raw_prog}'，默认为 0")
            base_progress = 0
    else:
        base_progress = 100 if is_completed else 0

    # 计算日期范围的总天数（用于进度递增）
    total_days = len(date_list)

    # 为每个日期创建任务，并自动递增进度
    tasks = []
    for idx, date_str in enumerate(date_list):
        # 性能优化：使用本地缓存判断工作日，避免频繁 API 调用
        # 统一使用 LocalFileService 进行节假日判断
        from mcp_server.services.local_fs import LocalFileService
        is_holiday, _ = LocalFileService.is_holiday(date_str)
        if is_holiday:
            logger.debug(f"[_parse_line] 跳过非工作日: {date_str}")
            continue

        # 计算当前日期的进度（线性递增）
        if total_days > 1 and not is_completed:
            # 进度从 base_progress 线性递增到 90%
            if total_days == 1:
                current_progress = base_progress
            else:
                # 简单的线性插值
                progress_step = (90 - base_progress) / (total_days - 1)
                current_progress = int(base_progress + progress_step * idx)
        else:
            current_progress = base_progress

        task_dict = {
            "content": content,
            "progress": current_progress,
            "date": date_str,
            "is_completed": is_completed,
        }
        tasks.append(task_dict)

        logger.debug(f"   📅 {date_str}: 进度={current_progress}%")

    logger.debug(f"[_parse_line] 出参: 共 {len(tasks)} 个任务")
    return tasks


class TodoParser:
    @staticmethod
    def is_task_message(text: str) -> bool:
        """
        判断文本是否为任务消息。
        
        Args:
            text (str): 待判断的文本内容。
            
        Returns:
            bool: 如果是任务消息返回 True，否则返回 False。
        """
        logger.debug(f"[TodoParser.is_task_message] 入参: text='{text[:50]}...' (len={len(text)})")

        if not text or not text.strip():
            logger.debug(f"[TodoParser.is_task_message] 文本为空，返回 False")
            return False

        stripped = text.strip().upper()
        if stripped in ("Y", "N", "YES", "NO", "是", "否", "确认", "取消"):
            logger.debug(f"[TodoParser.is_task_message] 命中简短回复关键词，返回 False")
            return False

        lines = [ln for ln in text.splitlines() if ln.strip()]
        if not lines:
            logger.debug(f"[TodoParser.is_task_message] 无有效行，返回 False")
            return False

        task_lines = sum(1 for ln in lines if _TASK_LINE_HINT.match(ln))
        total_lines = len(lines)
        ratio = task_lines / total_lines if total_lines > 0 else 0

        is_task = task_lines >= 1 and ratio > 0.5
        logger.debug(
            f"[TodoParser.is_task_message] 总行数: {total_lines}, 任务行数: {task_lines}, 比例: {ratio:.2f}, 结果: {is_task}")
        return is_task

    @classmethod
    def parse_message(cls, text: str) -> list[dict]:
        """
        解析消息中的任务列表。
        
        Args:
            text (str): 包含任务信息的原始消息文本。
            
        Returns:
            list[dict]: 解析出的任务字典列表。
        """
        logger.info(f"[TodoParser.parse_message] 入参: text='{text[:100]}...' (len={len(text)})")

        if not text:
            logger.debug(f"[TodoParser.parse_message] 文本为空，返回空列表")
            return []

        now_dt = datetime.now()
        tasks = []

        for i, line in enumerate(text.splitlines()):
            # _parse_line 现在返回任务列表（支持日期范围拆分）
            task_list = _parse_line(line, now_dt)
            if task_list:
                for task in task_list:
                    tasks.append(task)
                    logger.debug(
                        f"[TodoParser.parse_message] 第 {i + 1} 行解析成功: {task['content']} @ {task['date']}")

        logger.info(f"[TodoParser.parse_message] 出参: 共解析到 {len(tasks)} 条任务")
        return tasks
