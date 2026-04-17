import logging
import logging.config
import logging.handlers
from pathlib import Path

import yaml


def setup_logging():
    """初始化基于 YAML 的全局日志配置"""
    base_dir = Path(__file__).resolve().parent.parent
    log_dir = base_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    config_path = base_dir / "logging.yaml"

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            # 将 YAML 中的相对路径覆盖为绝对路径
            if "handlers" in config and "file" in config["handlers"]:
                config["handlers"]["file"]["filename"] = str(log_dir / "agent.log")

            logging.config.dictConfig(config)
        except Exception as e:
            logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
            logging.error(f"解析 logging.yaml 失败，已降级为基础日志: {e}")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        logging.warning("未找到 logging.yaml，使用默认控制台日志配置")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


# 模块加载时自动初始化
setup_logging()
