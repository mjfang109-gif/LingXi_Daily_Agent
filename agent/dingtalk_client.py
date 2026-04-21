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

                    # 核心修改：子线程执行多天实时预览生成（并行优化）
                    def _send_realtime_previews():
                        logger.info(f"🚀 [实时预览线程启动] 用户: {sender_id}")
                        try:
                            from agent.llm_client import ReportGenerator
                            from datetime import datetime
                            from concurrent.futures import ThreadPoolExecutor, as_completed

                            # 1. 先清理过期任务（与最终发送保持一致）
                            UserStore.clean_outdated(sender_id)
                            
                            # 2. 获取最新任务
                            all_tasks = UserStore.get_tasks(sender_id)

                            if not all_tasks:
                                logger.warning("⚠️ [实时预览] 无有效任务，跳过预览")
                                return

                            # 3. 提取不重复的日期
                            unique_dates = sorted(list(set(t["date"] for t in all_tasks)))
                            logger.info(f"📅 [实时预览] 检测到 {len(unique_dates)} 个有效日期: {unique_dates}")

                            # 4. 定义单个日期的生成函数
                            def generate_report_for_date(date_str: str) -> dict:
                                """为指定日期生成日报"""
                                today_t = [t for t in all_tasks if t["date"] == date_str]
                                future_t = [t for t in all_tasks if t["date"] > date_str]

                                # 获取当前任务版本
                                current_version = UserStore.get_task_version(sender_id)
                                
                                # 尝试从缓存中获取日报
                                cached_report = UserStore.get_cached_report(sender_id, date_str, current_version)
                                
                                if cached_report:
                                    logger.info(f"✅ [实时预览] 命中缓存: {date_str} (v{current_version})")
                                    report = cached_report
                                else:
                                    logger.info(f"🤖 [LLM] 生成 {date_str} 日报... (今日:{len(today_t)}, 未来:{len(future_t)})")
                                    report = ReportGenerator().generate(today_t, future_t)
                                    # 缓存生成的日报
                                    UserStore.cache_report(sender_id, date_str, report, current_version)
                                    logger.info(f"💾 [实时预览] 已缓存日报: {date_str} (v{current_version})")
                                
                                return {
                                    "date_str": date_str,
                                    "report": report,
                                    "today_t_count": len(today_t),
                                    "future_t_count": len(future_t)
                                }

                            # 5. 并行生成所有日期的日报
                            reports_data = []
                            max_workers = min(len(unique_dates), 5)  # 最多5个并发
                            logger.info(f"⚡ [并行优化] 使用 {max_workers} 个工作线程并行生成日报")
                            
                            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                                # 提交所有任务
                                future_to_date = {
                                    executor.submit(generate_report_for_date, date_str): date_str
                                    for date_str in unique_dates
                                }
                                
                                # 收集结果
                                for future in as_completed(future_to_date):
                                    date_str = future_to_date[future]
                                    try:
                                        result = future.result()
                                        reports_data.append(result)
                                        logger.info(f"   ✅ [{date_str}] 生成完成")
                                    except Exception as e:
                                        logger.error(f"   ❌ [{date_str}] 生成失败: {e}")

                            # 6. 按日期排序并发送卡片
                            reports_data.sort(key=lambda x: x["date_str"])
                            
                            for item in reports_data:
                                date_str = item["date_str"]
                                report = item["report"]
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

        # 关键修复：注册回调函数到 MCP 服务层
        logger.info("📝 注册消息监听回调函数...")
        self._get_service().start_message_listener(handle_incoming_message)
        logger.info("✅ 消息监听器已启动")

    def send_markdown_text_to_user(self, content: str, user_id: str | None = None) -> bool:
        """发送纯 Markdown 文本消息（用于闲聊或简单通知）"""
        try:
            return self._get_service().send_markdown_text_to_user(content, user_id=user_id)
        except Exception as e:
            logger.error(f"❌ [SendMarkdown] 异常: {e}")
            return False
