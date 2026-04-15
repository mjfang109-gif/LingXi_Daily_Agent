import os

import yaml
from dotenv import load_dotenv

load_dotenv()


class Config:
    # 敏感信息从环境变量读取
    APP_KEY = os.getenv("DINGTALK_APP_KEY")
    APP_SECRET = os.getenv("DINGTALK_APP_SECRET")
    USER_PHONE = os.getenv("DINGTALK_USER_PHONE")

    # 动态获取的 ID (初始运行工具后填入 .env)
    USER_ID = os.getenv("DINGTALK_USER_ID")
    TEMPLATE_ID = os.getenv("DINGTALK_TEMPLATE_ID")

    # 业务配置从 YAML 读取
    _yaml_config = {}

    @classmethod
    def load(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base_dir, 'config.yaml'), 'r', encoding='utf-8') as f:
            cls._yaml_config = yaml.safe_load(f)

    @classmethod
    def get(cls, key_path, default=None):
        """通过路径获取配置，如 'scheduler.report_time'"""
        keys = key_path.split('.')
        value = cls._yaml_config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default


# 初始化加载
Config.load()
