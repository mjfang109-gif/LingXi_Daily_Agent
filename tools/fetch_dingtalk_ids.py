import os
import sys

import requests

# 临时导入路径以使用 Config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.config_loader import Config
from common.logger import setup_logging, get_logger

setup_logging()
logger = get_logger("Init_Tool")


def fetch_ids():
    # 1. 获取 Token
    token_url = f"https://oapi.dingtalk.com/gettoken?appkey={Config.APP_KEY}&appsecret={Config.APP_SECRET}"
    token = requests.get(token_url).json().get("access_token")

    # 2. 根据手机号获取 UserID
    userid_url = f"https://oapi.dingtalk.com/topapi/v2/user/getbymobile?access_token={token}"
    user_res = requests.post(userid_url, json={"mobile": Config.USER_PHONE}).json()
    user_id = user_res.get("result", {}).get("userid")

    # 3. 获取日志模板列表
    template_url = f"https://oapi.dingtalk.com/topapi/report/template/getobjects?access_token={token}"
    tpl_res = requests.post(template_url, json={"userid": user_id}).json()
    templates = tpl_res.get("result", [])

    print("\n" + "=" * 50)
    print(f"👉 您的钉钉 UserID: {user_id}")
    print("-" * 50)
    print("📋 您可见的日志模板列表:")
    for t in templates:
        print(f"模板名称: {t['name']} | 模板ID: {t['template_id']}")
    print("=" * 50)
    print("\n请将上述 UserID 和您需要的 模板ID 写入您的 .env 文件中。")


if __name__ == "__main__":
    fetch_ids()
