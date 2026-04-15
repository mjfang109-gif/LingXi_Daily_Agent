import re
from common.logger import get_logger

logger = get_logger("Parser")


class TodoParser:
    # 序号. 任务内容 @日期 @状态 (进度XX%)
    PATTERN = re.compile(r'^\d+[\.、]\s*(.*?)(?:，进度(\d+)%)?(?:@([\d\.-]+))?(?:@(已完成|未完成))?$')

    @staticmethod
    def generate_progress_bar(percent):
        """生成文本进度条: ▓▓▓░░"""
        length = 10
        filled = int(length * percent / 100)
        return "▓" * filled + "░" * (length - filled)

    @classmethod
    def parse_file(cls, file_path):
        tasks = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    match = cls.PATTERN.match(line.strip())
                    if match:
                        content = match.group(1).strip()
                        progress = int(match.group(2)) if match.group(2) else (100 if match.group(4) != "未完成" else 0)
                        date = match.group(3)
                        is_done = False if match.group(4) == "未完成" else True

                        tasks.append({
                            "content": content,
                            "progress": progress,
                            "bar": cls.generate_progress_bar(progress),
                            "date": date,
                            "is_completed": is_done
                        })
            return tasks
        except Exception as e:
            logger.error(f"解析失败: {e}")
            return []
