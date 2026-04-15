import os

import yaml
from dotenv import load_dotenv

load_dotenv()


class Config:
    # --- 钉钉应用凭证 (用于事件订阅和API调用) ---
    CLIENT_ID = os.getenv("DINGTALK_CLIENT_ID")
    CLIENT_SECRET = os.getenv("DINGTALK_CLIENT_SECRET")
    
    # --- 机器人和对话信息 ---
    ROBOT_CODE = os.getenv("DINGTALK_ROBOT_CODE") # 机器人自身的Code
    CHAT_ID = os.getenv("DINGTALK_CHAT_ID")       # 接收日报的群聊ID
    USER_ID = os.getenv("DINGTALK_USER_ID")       # 接收日报的群聊ID

    # --- 钉钉回调配置 (用于互动卡片) ---
    # 这个URL需要是公网可访问的，钉钉服务器会向这个地址发送回调事件
    CALLBACK_URL_BASE = os.getenv("DINGTALK_CALLBACK_URL_BASE")

    # --- LLM 相关配置 ---
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL")
    LLM_MODEL = os.getenv("LLM_MODEL")


    # --- 业务配置从 YAML 读取 ---
    _yaml_config = {}

    @classmethod
    def load(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, 'config.yaml')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
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
