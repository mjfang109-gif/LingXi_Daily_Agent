import os
import yaml
import logging
import logging.config


def setup_logging():
    """初始化基于 YAML 的全局日志配置"""
    # 动态获取工程根目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(base_dir, 'logs')

    # 确保日志目录存在
    os.makedirs(log_dir, exist_ok=True)

    config_path = os.path.join(base_dir, 'logging.yaml')

    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            # 动态覆盖 YAML 中的相对路径为绝对路径，防止进程启动位置不同导致日志乱跑
            if 'handlers' in config and 'file' in config['handlers']:
                config['handlers']['file']['filename'] = os.path.join(log_dir, 'agent.log')

            logging.config.dictConfig(config)
        except Exception as e:
            # 降级处理：如果 YAML 写错了，不能让程序起不来
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.error(f"解析 logging.yaml 失败，已降级为基础日志。错误信息: {e}")
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.warning("未找到 logging.yaml，使用默认控制台日志配置")


def get_logger(name: str) -> logging.Logger:
    """获取指定模块的日志记录器"""
    return logging.getLogger(name)


# 导入时自动初始化一次，确保所有依赖此模块的文件都能拿到正确的配置
setup_logging()
