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

    def send_card_to_user(self, *args, **kwargs) -> bool:
        try:
            return self._get_service().send_card_to_user(*args, **kwargs)
        except Exception:
            return False

    def send_text_to_user(self, content: str, user_id: str | None = None) -> bool:
        try:
            return self._get_service().send_text_to_user(content, user_id=user_id)
        except Exception:
            return False

    def send_result_card_to_user(self, *args, **kwargs) -> bool:
        try:
            return self._get_service().send_result_card_to_user(*args, **kwargs)
        except Exception:
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

                    # 核心修改：子线程执行多天实时预览生成
                    def _send_realtime_previews():
                        from agent.llm_client import ReportGenerator, build_summary_card
                        # 提取所有不重复的日期
                        unique_dates = sorted(list(set(t["date"] for t in all_tasks)))

                        for date_str in unique_dates:
                            # 按照特定日期分组任务（今天 vs 未来）
                            today_t = [t for t in all_tasks if t["date"] == date_str]
                            future_t = [t for t in all_tasks if t["date"] > date_str]

                            report = ReportGenerator().generate(today_t, future_t)
                            summary = build_summary_card(today_t + future_t)

                            title = f"👀 实时日报预览 ({date_str})"
                            self.send_card_to_user(
                                title=title,
                                today_work=report.get("today_work", "（无）"),
                                tomorrow_plan=report.get("tomorrow_plan", "（无）"),
                                summary_card=summary,
                                mode="preview",  # 启用预览沙箱模式
                                user_id=sender_id
                            )

                    threading.Thread(target=_send_realtime_previews, daemon=True).start()
                return

            def _process_ai_chat():
                engine = AIChatEngine()
                ai_reply = engine.chat(raw_text)
                self.send_text_to_user(ai_reply, user_id=sender_id)

            threading.Thread(target=_process_ai_chat, daemon=True).start()

        try:
            self._get_service().start_message_listener(on_message_callback=handle_incoming_message)
        except Exception as e:
            logger.error(f"❌ 启动 Stream 监听失败: {e}")
            raise
