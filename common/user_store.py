"""
UserStore — 多用户会话管理
新增：过期任务的垃圾回收机制（clean_outdated_tasks）
"""
import queue
import threading
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("UserStore")


@dataclass
class UserSession:
    user_id: str
    tasks: list = field(default_factory=list)
    task_version: int = 0
    confirm_queue: queue.Queue = field(default_factory=queue.Queue)
    template_id: str = ""
    contents_config: list = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def merge_tasks(self, new_tasks: list) -> int:
        with self._lock:
            existing_by_content = {t["content"]: (i, t) for i, t in enumerate(self.tasks)}
            updated = False
            for t in new_tasks:
                key = t["content"]
                if key in existing_by_content:
                    idx, old = existing_by_content[key]
                    if old != t:
                        self.tasks[idx] = t
                        existing_by_content[key] = (idx, t)
                        updated = True
                else:
                    self.tasks.append(t)
                    existing_by_content[key] = (len(self.tasks) - 1, t)
                    updated = True

            if updated: self.task_version += 1
            return self.task_version

    def clean_outdated_tasks(self) -> int:
        """核心修改：删除所有日期小于今天的过期任务"""
        today_str = datetime.now().strftime("%Y-%m-%d")
        with self._lock:
            valid_tasks = [t for t in self.tasks if t["date"] >= today_str]
            if len(valid_tasks) != len(self.tasks):
                logger.info(f"🗑️ 已自动清理 {len(self.tasks) - len(valid_tasks)} 条过期任务")
                self.tasks = valid_tasks
                self.task_version += 1
            return self.task_version

    def clear_tasks(self):
        with self._lock:
            self.tasks.clear()
            self.task_version += 1


class UserStore:
    _sessions: dict[str, UserSession] = {}
    _store_lock = threading.Lock()

    @classmethod
    def _load_user_config(cls, user_id: str) -> dict:
        users_cfg = Config.get("users", []) or []
        for u in users_cfg:
            if u.get("user_id") == user_id:
                return u
        return {}

    @classmethod
    def get_or_create(cls, user_id: str) -> UserSession:
        with cls._store_lock:
            if user_id not in cls._sessions:
                cfg = cls._load_user_config(user_id)
                session = UserSession(
                    user_id=user_id,
                    template_id=cfg.get("template_id", Config.TEMPLATE_ID or ""),
                    contents_config=cfg.get("contents", []),
                )
                cls._sessions[user_id] = session
            return cls._sessions[user_id]

    @classmethod
    def get(cls, user_id: str) -> Optional[UserSession]:
        return cls._sessions.get(user_id)

    @classmethod
    def all_user_ids(cls) -> list[str]:
        cfg_ids = [u["user_id"] for u in (Config.get("users", []) or []) if u.get("user_id")]
        runtime_ids = list(cls._sessions.keys())
        return list(dict.fromkeys(cfg_ids + runtime_ids))

    @classmethod
    def merge_tasks(cls, user_id: str, new_tasks: list) -> int:
        session = cls.get_or_create(user_id)
        version = session.merge_tasks(new_tasks)
        return version

    @classmethod
    def clean_outdated(cls, user_id: str):
        """暴露清理过期的接口"""
        session = cls.get(user_id)
        if session: session.clean_outdated_tasks()

    @classmethod
    def get_tasks(cls, user_id: str) -> list:
        session = cls.get(user_id)
        return list(session.tasks) if session else []

    @classmethod
    def get_task_version(cls, user_id: str) -> int:
        session = cls.get(user_id)
        return session.task_version if session else 0

    @classmethod
    def put_response(cls, user_id: str, response: str):
        session = cls.get_or_create(user_id)
        session.confirm_queue.put_nowait(response)

    @classmethod
    def get_response_nowait(cls, user_id: str) -> Optional[str]:
        session = cls.get(user_id)
        if session is None: return None
        try:
            return session.confirm_queue.get_nowait()
        except queue.Empty:
            return None

    @classmethod
    def get_template_id(cls, user_id: str) -> str:
        session = cls.get_or_create(user_id)
        return session.template_id or Config.TEMPLATE_ID or ""

    @classmethod
    def get_contents_config(cls, user_id: str) -> list:
        session = cls.get_or_create(user_id)
        return session.contents_config or []
