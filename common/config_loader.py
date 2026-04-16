import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ── 钉钉应用凭证 ──────────────────────────────────────────
    CLIENT_ID = os.getenv("DINGTALK_CLIENT_ID")
    CLIENT_SECRET = os.getenv("DINGTALK_CLIENT_SECRET")

    # ── 机器人和用户信息 ──────────────────────────────────────
    ROBOT_CODE = os.getenv("DINGTALK_ROBOT_CODE")  # 用于单聊发卡片
    USER_ID = os.getenv("DINGTALK_USER_ID")  # 接收预览的用户
    TEMPLATE_ID = os.getenv("DINGTALK_TEMPLATE_ID")  # 日报模版 ID

    # ── LLM ──────────────────────────────────────────────────
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

    # ── YAML 业务配置（懒加载） ───────────────────────────────
    _yaml_config: dict = {}

    @classmethod
    def load(cls):
        base_dir = Path(__file__).resolve().parent.parent
        config_path = base_dir / "config.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                cls._yaml_config = yaml.safe_load(f) or {}

    @classmethod
    def get(cls, key_path: str, default=None):
        """点分路径读取 YAML 配置，如 'scheduler.report_time'"""
        keys = key_path.split(".")
        value = cls._yaml_config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default


# 模块加载时自动初始化
Config.load()
