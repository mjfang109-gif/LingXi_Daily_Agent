"""
UserStore — 多用户会话管理
新增：过期任务的垃圾回收机制（clean_outdated_tasks）
"""
import json
import queue
import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

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
    # 新增：模板缓存 {template_id: {"name": "...", "contents": [...]}}
    templates_cache: dict = field(default_factory=dict)
    default_template_id: str = ""  # 用户的默认模板（最近使用的）
    last_active: datetime = field(default_factory=datetime.now)  # 最后活动时间，用于清理闲置会话

    def merge_tasks(self, new_tasks: list) -> int:
        """
        合并新任务到当前会话的任务列表中。

        逻辑：
        1. 基于任务内容+日期（content+date）进行去重和更新。
        2. 如果新任务的内容+日期已存在，且任务详情不同，则更新现有任务。
        3. 如果新任务的内容+日期不存在，则追加到列表末尾。
        4. 如果有任务被新增或更新，则增加 task_version 版本号。

        Args:
            new_tasks (list): 新的任务列表，每个任务为包含 'content', 'date' 等字段的字典。

        Returns:
            int: 当前的任务版本号。
        """
        with self._lock:
            # 构建现有任务的索引映射：{content_date_key: (index, task_dict)}
            existing_by_key = {}
            for i, t in enumerate(self.tasks):
                key = f"{t['content']}_{t['date']}"
                existing_by_key[key] = (i, t)

            updated = False

            for t in new_tasks:
                # 使用 content + date 作为唯一键
                key = f"{t['content']}_{t['date']}"

                if key in existing_by_key:
                    idx, old_task = existing_by_key[key]
                    # 明确定义需要追踪的字段，避免字典浅比较的不确定性
                    task_changed = (
                        old_task.get('content') != t.get('content') or
                        old_task.get('progress') != t.get('progress') or
                        old_task.get('is_completed') != t.get('is_completed') or
                        old_task.get('date') != t.get('date')
                    )
                    
                    if task_changed:
                        self.tasks[idx] = t
                        existing_by_key[key] = (idx, t)
                        updated = True
                        logger.debug(f"🔄 更新任务: {t['content']} @ {t['date']}")
                else:
                    # 新任务，追加到列表
                    self.tasks.append(t)
                    existing_by_key[key] = (len(self.tasks) - 1, t)
                    updated = True
                    logger.debug(f"➕ 新增任务: {t['content']} @ {t['date']}")

            # 仅在有变更时递增版本号
            if updated:
                self.task_version += 1
                logger.info(f"📊 任务版本更新至 v{self.task_version}")

            return self.task_version

    def clean_outdated_tasks(self) -> int:
        """
        清理过期的任务。
        
        逻辑：
        1. 获取当前日期字符串（格式：YYYY-MM-DD）。
        2. 遍历当前会话的所有任务，保留日期大于或等于今天日期的任务。
        3. 如果有任务被清理，则更新任务列表并递增 task_version 版本号。
        
        Returns:
            int: 当前的任务版本号。
        """
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
    """
    用户会话存储管理类。
    负责管理多用户的会话状态、任务合并、模板缓存及配置读取。
    采用单例模式（通过类变量和类方法实现），确保全局只有一个会话存储实例。
    """
    # 存储所有活跃用户的会话对象，key为user_id，value为UserSession实例
    _sessions: dict[str, UserSession] = {}
    # 用于保护 _sessions 字典读写操作的线程锁，防止并发修改导致的数据竞争
    _store_lock = threading.Lock()

    @classmethod
    def _load_user_config(cls, user_id: str) -> dict:
        """
        从全局配置中加载指定用户的个性化配置。
        
        Args:
            user_id (str): 用户唯一标识。
            
        Returns:
            dict: 用户配置字典，如果未找到则返回空字典。
        """
        # 获取配置中的 users 列表，如果不存在则默认为空列表
        users_cfg = Config.get("users", []) or []
        # 遍历用户列表，查找匹配 user_id 的配置项
        for u in users_cfg:
            if u.get("user_id") == user_id:
                # 找到匹配项，直接返回该用户的配置
                return u
        # 未找到匹配项，返回空字典
        return {}

    @classmethod
    def get_or_create(cls, user_id: str) -> UserSession:
        """
        获取指定用户的会话对象，如果不存在则创建一个新的会话。
        这是一个线程安全的方法。
        
        Args:
            user_id (str): 用户唯一标识。
            
        Returns:
            UserSession: 对应用户的会话对象。
        """
        # 加锁以确保在检查和创建会话时的原子性，防止多线程同时创建同一用户的会话
        with cls._store_lock:
            # 检查会话是否已存在
            if user_id not in cls._sessions:
                # 加载用户个性化配置
                cfg = cls._load_user_config(user_id)
                # 创建新的 UserSession 实例
                session = UserSession(
                    user_id=user_id,
                    # 优先使用用户配置中的 template_id，否则使用全局默认 TEMPLATE_ID，最后兜底为空字符串
                    template_id=cfg.get("template_id", Config.TEMPLATE_ID or ""),
                    # 使用用户配置中的 contents 列表，默认为空列表
                    contents_config=cfg.get("contents", []),
                )
                # 将新创建的会话存入全局字典
                cls._sessions[user_id] = session
            # 返回已存在或刚创建的会话对象
            return cls._sessions[user_id]

    @classmethod
    def get(cls, user_id: str) -> Optional[UserSession]:
        """
        获取指定用户的会话对象，如果不存在则返回 None。
        
        Args:
            user_id (str): 用户唯一标识。
            
        Returns:
            Optional[UserSession]: 会话对象或 None。
        """
        # 直接从字典中获取，不存在则返回 None
        return cls._sessions.get(user_id)

    @classmethod
    def all_user_ids(cls) -> list[str]:
        """
        获取所有已知用户的 ID 列表。
        包括配置文件中定义的用户和当前运行时已创建会话的用户。
        
        Returns:
            list[str]: 去重后的用户 ID 列表。
        """
        # 从配置文件中提取所有定义了 user_id 的用户 ID
        cfg_ids = [u["user_id"] for u in (Config.get("users", []) or []) if u.get("user_id")]
        # 获取当前运行时内存中已存在的会话用户 ID
        runtime_ids = list(cls._sessions.keys())
        # 合并两个列表，并使用 dict.fromkeys 进行去重且保持顺序，最后转为列表返回
        return list(dict.fromkeys(cfg_ids + runtime_ids))

    @classmethod
    def merge_tasks(cls, user_id: str, new_tasks: list) -> int:
        """
        合并新任务到指定用户的会话中。
        
        Args:
            user_id (str): 用户唯一标识。
            new_tasks (list): 新任务列表。
            
        Returns:
            int: 合并后的任务版本号。
        """
        # 获取或创建用户会话
        session = cls.get_or_create(user_id)
        # 调用会话对象的 merge_tasks 方法进行实际合并
        version = session.merge_tasks(new_tasks)
        # 更新最后活动时间
        session.last_active = datetime.now()
        return version

    @classmethod
    def clean_outdated(cls, user_id: str):
        """
        清理指定用户会话中的过期任务。
        
        Args:
            user_id (str): 用户唯一标识。
        """
        # 获取用户会话，如果用户不存在则不执行任何操作
        session = cls.get(user_id)
        if session:
            # 调用会话对象的清理方法
            session.clean_outdated_tasks()

    @classmethod
    def get_tasks(cls, user_id: str) -> list:
        """
        获取指定用户当前的所有任务列表。
        
        Args:
            user_id (str): 用户唯一标识。
            
        Returns:
            list: 任务列表的副本，如果用户不存在则返回空列表。
        """
        session = cls.get(user_id)
        # 如果会话存在，返回任务列表的浅拷贝，避免外部直接修改内部状态；否则返回空列表
        return list(session.tasks) if session else []

    @classmethod
    def get_task_version(cls, user_id: str) -> int:
        """
        获取指定用户任务列表的版本号。
        
        Args:
            user_id (str): 用户唯一标识。
            
        Returns:
            int: 任务版本号，如果用户不存在则返回 0。
        """
        session = cls.get(user_id)
        # 如果会话存在，返回版本号；否则返回 0
        return session.task_version if session else 0

    @classmethod
    def put_response(cls, user_id: str, response: str):
        """
        将响应消息放入指定用户的确认队列中。
        
        Args:
            user_id (str): 用户唯一标识。
            response (str): 响应消息内容。
        """
        # 获取或创建用户会话
        session = cls.get_or_create(user_id)
        # 非阻塞地将消息放入队列
        session.confirm_queue.put_nowait(response)

    @classmethod
    def get_response_nowait(cls, user_id: str) -> Optional[str]:
        """
        非阻塞地从指定用户的确认队列中获取一条响应消息。
        
        Args:
            user_id (str): 用户唯一标识。
            
        Returns:
            Optional[str]: 队列中的消息，如果队列为空或用户不存在则返回 None。
        """
        session = cls.get(user_id)
        # 如果会话不存在，直接返回 None
        if session is None:
            return None
        try:
            # 尝试非阻塞地获取队列中的消息
            response = session.confirm_queue.get_nowait()
            # 更新最后活动时间
            session.last_active = datetime.now()
            return response
        except queue.Empty:
            # 如果队列为空，捕获异常并返回 None
            return None

    @classmethod
    def get_template_id(cls, user_id: str) -> str:
        """
        获取指定用户当前使用的模板 ID。
        
        Args:
            user_id (str): 用户唯一标识。
            
        Returns:
            str: 模板 ID，优先级：会话中的 template_id > 全局默认 TEMPLATE_ID > 空字符串。
        """
        session = cls.get_or_create(user_id)
        # 返回会话中的 template_id，如果为空则尝试使用全局默认值，最后兜底为空字符串
        return session.template_id or Config.TEMPLATE_ID or ""

    @classmethod
    def get_contents_config(cls, user_id: str) -> list:
        """
        获取指定用户的内容配置列表。
        
        Args:
            user_id (str): 用户唯一标识。
            
        Returns:
            list: 内容配置列表，如果为空则返回空列表。
        """
        session = cls.get_or_create(user_id)
        # 返回会话中的 contents_config，如果为 None 或空则返回空列表
        return session.contents_config or []

    @classmethod
    def cache_user_templates(cls, user_id: str, templates: list) -> None:
        """
        缓存用户的模板列表及字段结构，并智能识别默认模板。

        Args:
            user_id (str): 用户唯一标识。
            templates (list): 模板列表，每个元素为包含 template_id, template_name, contents 等的字典。
        """
        logger.info(f"[cache_user_templates] 开始缓存 | 用户: {user_id}, 模板数: {len(templates)}")

        # 获取或创建用户会话
        session = cls.get_or_create(user_id)

        # 获取用于识别日报模板的关键词列表，默认为 ["日报", "每日", "Daily"]
        report_keywords = Config.get("dingtalk.daily_report_name_keywords", ["日报", "每日", "Daily"])
        logger.debug(f"[cache_user_templates] 日报关键词: {report_keywords}")

        # 加锁以保护会话内部的 templates_cache 和 default_template_id 等状态的修改
        with session._lock:
            daily_report_tmpl_id = None

            logger.info(f"[cache_user_templates] 开始遍历 {len(templates)} 个模板")

            # 遍历传入的模板列表
            for idx, tmpl in enumerate(templates):
                logger.debug(f"[cache_user_templates] 处理模板 #{idx + 1}: {json.dumps(tmpl, ensure_ascii=False)}")

                # 根据实际测试，钉钉API返回的字段名为 template_id
                tmpl_id = tmpl.get("template_id")
                
                # 兼容 template_name 和 name 两种字段名
                tmpl_name = tmpl.get("template_name") or tmpl.get("name", "")

                logger.info(f"   模板 #{idx + 1}: ID={tmpl_id}, 名称={tmpl_name}")

                # 只有当 template_id 存在时才处理
                if not tmpl_id:
                    logger.warning(f"   ⚠️ 模板 #{idx + 1} 缺少 template_id，原始数据: {json.dumps(tmpl, ensure_ascii=False)}")
                    continue

                # 将模板信息存入会话的缓存字典中
                session.templates_cache[tmpl_id] = {
                    "name": tmpl_name,
                    "contents": tmpl.get("contents", []),
                }

                logger.info(f"   ✅ 已缓存模板 '{tmpl_name}' ({len(tmpl.get('contents', []))} 个字段)")

                # 检查模板名称是否包含日报关键词（不区分大小写）
                if any(keyword.lower() in tmpl_name.lower() for keyword in report_keywords):
                    # 如果尚未找到日报模板，则记录当前匹配的模板 ID（取第一个匹配的）
                    if daily_report_tmpl_id is None:
                        daily_report_tmpl_id = tmpl_id
                        logger.info(f"🎯 为用户 {user_id} 识别到日报模板: {tmpl_name} ({tmpl_id})")

            # 设置默认模板的逻辑，优先级：识别到的日报模板 > 列表中的第一个模板 > 保持原有配置
            if daily_report_tmpl_id:
                # 如果识别到了日报模板，将其设为默认模板
                session.default_template_id = daily_report_tmpl_id
                session.template_id = daily_report_tmpl_id
                logger.info(f"✅ 已为用户 {user_id} 设置日报模板为默认: {daily_report_tmpl_id}")
            elif not session.default_template_id and templates:
                # 如果没有识别到日报模板，且当前没有默认模板，且传入的模板列表不为空
                # 则使用列表中的第一个模板作为默认模板
                first_tmpl_id = templates[0].get("template_id", "")
                if first_tmpl_id:
                    session.default_template_id = first_tmpl_id
                    session.template_id = first_tmpl_id
                    logger.info(f"✅ 已为用户 {user_id} 设置第一个模板为默认: {first_tmpl_id}")

            # 记录缓存完成的日志
            logger.info(f"💾 已为用户 {user_id} 缓存 {len(session.templates_cache)} 个模板")
            logger.debug(f"[cache_user_templates] 缓存内容: {session.templates_cache}")

    @classmethod
    def get_template_contents(cls, user_id: str, template_id: str | None = None) -> list:
        """
        获取指定模板的字段配置。
        优先级：指定的模板ID/默认模板ID对应的缓存 > 用户默认配置 > 全局默认配置。
        
        Args:
            user_id (str): 用户唯一标识。
            template_id (str | None): 可选，指定要获取的模板 ID。如果为 None，则使用默认模板。
            
        Returns:
            list: 模板的字段配置列表。
        """
        session = cls.get_or_create(user_id)

        # 确定目标模板 ID：优先使用参数传入的，其次是会话中的默认模板 ID，最后是会话中的当前模板 ID
        target_tmpl_id = template_id or session.default_template_id or session.template_id

        # 1. 尝试从缓存中获取目标模板的内容
        if target_tmpl_id and target_tmpl_id in session.templates_cache:
            cached = session.templates_cache[target_tmpl_id]
            contents = cached.get("contents", [])
            # 如果缓存中存在有效的内容列表，则直接返回
            if contents:
                logger.debug(f"📋 使用缓存模板: {cached.get('name', '')} ({target_tmpl_id})")
                return contents

        # 2. 如果缓存中未找到，降级使用用户级别的默认内容配置
        if session.contents_config:
            logger.debug("📋 使用用户默认配置")
            return session.contents_config

        # 3. 如果用户也没有配置，降级使用全局默认配置（今日工作 + 明日计划）
        today_key = Config.get("dingtalk.report_field_today", "今日工作")
        tomorrow_key = Config.get("dingtalk.report_field_tomorrow", "明日计划")
        global_config = [
            {"sort": 1, "key": today_key},
            {"sort": 2, "key": tomorrow_key},
        ]
        logger.debug("📋 使用全局默认配置")
        return global_config

    @classmethod
    def set_default_template(cls, user_id: str, template_id: str) -> None:
        """
        手动设置指定用户的默认模板。
        
        Args:
            user_id (str): 用户唯一标识。
            template_id (str): 要设置为默认的模板 ID。
        """
        session = cls.get_or_create(user_id)
        # 加锁以保护会话状态的修改
        with session._lock:
            # 更新默认模板 ID 和当前使用的模板 ID
            session.default_template_id = template_id
            session.template_id = template_id
            logger.info(f"✅ 用户 {user_id} 默认模板已设置为 {template_id}")

    @classmethod
    def get_all_templates(cls, user_id: str) -> dict:
        """
        获取指定用户的所有缓存模板。
        
        Args:
            user_id (str): 用户唯一标识。
            
        Returns:
            dict: 模板缓存字典的副本，key 为 template_id，value 为模板详细信息。
        """
        session = cls.get_or_create(user_id)
        # 返回字典的浅拷贝，防止外部修改影响内部缓存
        return dict(session.templates_cache)

    @classmethod
    def cleanup_inactive_sessions(cls, max_idle_days: int = 30) -> int:
        """
        清理超过指定天数无活动的会话，防止内存泄漏。
        
        Args:
            max_idle_days (int): 最大闲置天数，默认 30 天。
            
        Returns:
            int: 清理的会话数量。
        """
        now = datetime.now()
        inactive_users = []
        
        with cls._store_lock:
            for uid, session in cls._sessions.items():
                idle_days = (now - session.last_active).days
                if idle_days > max_idle_days:
                    inactive_users.append(uid)
                    logger.info(f"🗑️ 检测到闲置会话: {uid}, 已闲置 {idle_days} 天")
            
            # 执行清理
            for uid in inactive_users:
                del cls._sessions[uid]
                logger.info(f"✅ 已清理闲置会话: {uid}")
        
        if inactive_users:
            logger.info(f"📊 共清理 {len(inactive_users)} 个闲置会话")
        
        return len(inactive_users)
