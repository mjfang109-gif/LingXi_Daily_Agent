"""
DingTalkClient — 钉钉客户端
新增：接收任务后触发独立的多天实时预览（且绝对安全隔离）
"""
import threading

from common.logger import get_logger

logger = get_logger("DingTalk_Client")


class DingTalkClient:
    def __init__(self):
        self._service_class = None

    def _get_service(self):
        if self._service_class is None:
            from mcp_server.services.dingtalk_message import DingTalkMessageService
            self._service_class = DingTalkMessageService
        return self._service_class

    @property
    def is_configured(self) -> bool:
        from common.config_loader import Config
        return bool(Config.CLIENT_ID and Config.CLIENT_SECRET and Config.ROBOT_CODE)

    def send_card_to_user(
            self,
            title: str,
            today_work: str,
            tomorrow_plan: str,
            countdown_min: int = 15,
            mode: str = "auto",
            user_id: str | None = None,
    ) -> bool:
        try:
            logger.info(f"  📤 [发送卡片] 准备发送预览卡片...")
            return self._get_service().send_card_to_user(
                title=title,
                today_work=today_work,
                tomorrow_plan=tomorrow_plan,
                countdown_min=countdown_min,
                mode=mode,
                user_id=user_id,
            )
        except Exception as e:
            logger.error(f"❌ [DingTalkClient.send_card_to_user] 调用异常: {e}", exc_info=True)
            import traceback
            logger.error(f"堆栈跟踪:\n{traceback.format_exc()}")
            return False

    def send_text_to_user(self, content: str, user_id: str | None = None) -> bool:
        try:
            return self._get_service().send_text_to_user(content, user_id=user_id)
        except Exception as e:
            logger.error(f"❌ [DingTalkClient.send_text_to_user] 调用异常: {e}", exc_info=True)
            return False

    def send_result_card_to_user(self, *args, **kwargs) -> bool:
        try:
            return self._get_service().send_result_card_to_user(*args, **kwargs)
        except Exception as e:
            logger.error(f"❌ [DingTalkClient.send_result_card_to_user] 调用异常: {e}", exc_info=True)
            return False

    def start_message_listener(self) -> None:
        from agent.parser import TodoParser
        from common.user_store import UserStore
        from common.config_loader import Config
        from agent.chat_engine import AIChatEngine

        def handle_incoming_message(sender_id: str, raw_text: str):
            upper_text = raw_text.upper()

            if upper_text in ("Y", "N", "YES", "NO", "是", "否", "确认", "取消"):
                normalized = "Y" if upper_text in ("Y", "YES", "是", "确认") else "N"
                UserStore.put_response(sender_id, normalized)
                return

            if TodoParser.is_task_message(raw_text):
                tasks = TodoParser.parse_message(raw_text)
                if tasks:
                    # 合并任务并立刻执行过期清理
                    UserStore.merge_tasks(sender_id, tasks)
                    UserStore.clean_outdated(sender_id)

                    all_tasks = UserStore.get_tasks(sender_id)
                    total = len(all_tasks)
                    report_time = Config.get("scheduler.report_time", "17:50")

                    self.send_text_to_user(
                        f"✅ 任务更新成功，已清理过期历史，当前共 {total} 条有效任务。\n"
                        f"⏳ 正在呼叫大模型生成多天日志预览，请稍候...\n"
                        f"（实际发送将在 {report_time} 触发，随时可追加）",
                        user_id=sender_id
                    )

                    # 核心修改：异步预加载用户模板（不阻塞主流程）
                    def _preload_templates():
                        from mcp_server.services.dingtalk_api import DingTalkService
                        try:
                            # 查询用户的所有模板
                            res = DingTalkService.get_report_templates(sender_id)
                            if res.get("success"):
                                templates = res.get("templates", [])

                                # 为每个模板查询详细字段结构
                                detailed_templates = []
                                for tmpl in templates:
                                    tmpl_id = tmpl.get("template_id")
                                    if tmpl_id:
                                        detail_res = DingTalkService.get_template_detail(sender_id, tmpl_id)
                                        if detail_res.get("success"):
                                            detailed_templates.append(detail_res)

                                # 缓存到 UserSession
                                if detailed_templates:
                                    UserStore.cache_user_templates(sender_id, detailed_templates)
                                    logger.info(f"✅ 已为用户 {sender_id} 预加载 {len(detailed_templates)} 个模板")
                        except Exception as e:
                            logger.warning(f"⚠️ 预加载模板失败: {e}，将使用配置兜底")

                    threading.Thread(target=_preload_templates, daemon=True).start()

                    # 核心修改：子线程执行多天实时预览生成
                    def _send_realtime_previews():
                        logger.info(f"🚀 [实时预览线程启动] 用户: {sender_id}")
                        try:
                            from agent.llm_client import ReportGenerator
                            from datetime import datetime

                            # 1. 获取最新任务
                            all_tasks = UserStore.get_tasks(sender_id)

                            # 2. 强制过滤过期任务 (双重保险)
                            today_str = datetime.now().strftime("%Y-%m-%d")
                            valid_tasks = [t for t in all_tasks if t["date"] >= today_str]

                            if not valid_tasks:
                                logger.warning("⚠️ [实时预览] 无有效未来任务，跳过预览")
                                return

                            # 3. 提取不重复的日期
                            unique_dates = sorted(list(set(t["date"] for t in valid_tasks)))
                            logger.info(f"📅 [实时预览] 检测到 {len(unique_dates)} 个有效日期: {unique_dates}")

                            for idx, date_str in enumerate(unique_dates):
                                # 按照特定日期分组
                                today_t = [t for t in valid_tasks if t["date"] == date_str]
                                future_t = [t for t in valid_tasks if t["date"] > date_str]

                                logger.info(
                                    f"🤖 [LLM] 生成 {date_str} 日报... (今日:{len(today_t)}, 未来:{len(future_t)})")
                                report = ReportGenerator().generate(today_t, future_t)

                                title = f"实时日报预览 ({date_str})"

                                # 发送 Markdown 卡片
                                success = self.send_card_to_user(
                                    title=title,
                                    today_work=report.get("today_work", "（无）"),
                                    tomorrow_plan=report.get("tomorrow_plan", "（无）"),
                                    mode="preview",
                                    user_id=sender_id
                                )
                                logger.info(f"   {'✅' if success else '❌'} [{date_str}] 预览发送结果")

                        except Exception as e:
                            logger.error(f"❌ [实时预览异常]: {e}", exc_info=True)

                    threading.Thread(target=_send_realtime_previews, daemon=True).start()
                return

            def _process_ai_chat():
                engine = AIChatEngine()
                ai_reply = engine.chat(raw_text)
                # 闲聊也使用 Markdown 发送，提升阅读体验
                self.send_markdown_text_to_user(ai_reply, user_id=sender_id)

            threading.Thread(target=_process_ai_chat, daemon=True).start()

    def send_markdown_text_to_user(self, content: str, user_id: str | None = None) -> bool:
        """发送纯 Markdown 文本消息（用于闲聊或简单通知）"""
        try:
            return self._get_service().send_markdown_text_to_user(content, user_id=user_id)
        except Exception as e:
            logger.error(f"❌ [SendMarkdown] 异常: {e}")
            return False
