"""
初始化工具 — 帮助用户一键获取钉钉 UserID 和日志模板列表
用法：python tools/fetch_dingtalk_ids.py [手机号]
"""
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.config_loader import Config
from common.logger import get_logger, setup_logging

setup_logging()
logger = get_logger("InitTool")


def fetch_ids(mobile: str | None = None):
    if not mobile:
        mobile = Config.get("dingtalk.user_phone") or input("请输入您的钉钉绑定手机号: ").strip()

    if not mobile:
        print("❌ 未提供手机号，退出")
        return

    print(f"\n🔍 正在查询手机号 {mobile} 对应的钉钉信息...\n")

    # 1. 获取 Token
    token_url = (
        f"https://oapi.dingtalk.com/gettoken"
        f"?appkey={Config.CLIENT_ID}&appsecret={Config.CLIENT_SECRET}"
    )
    token_resp = requests.get(token_url, timeout=10).json()
    if token_resp.get("errcode") != 0:
        print(f"❌ 获取 Token 失败: {token_resp.get('errmsg')}")
        return
    token = token_resp["access_token"]

    # 2. 根据手机号获取 UserID
    userid_url = f"https://oapi.dingtalk.com/topapi/v2/user/getbymobile?access_token={token}"
    user_resp = requests.post(userid_url, json={"mobile": mobile}, timeout=10).json()
    if user_resp.get("errcode") != 0:
        print(f"❌ 获取 UserID 失败: {user_resp.get('errmsg')}")
        return
    user_id = user_resp.get("result", {}).get("userid")

    # 3. 获取日志模板列表
    tpl_url = f"https://oapi.dingtalk.com/topapi/report/template/listbyuserid?access_token={token}"
    tpl_resp = requests.post(tpl_url, json={"userid": user_id, "offset": 0, "size": 100}, timeout=10).json()
    templates = tpl_resp.get("result", {}).get("template_list", []) if tpl_resp.get("errcode") == 0 else []

    print("=" * 55)
    print(f"  👤 UserID：{user_id}")
    print("-" * 55)
    print(f"  📋 可见日志模板列表（共 {len(templates)} 个）:")
    for t in templates:
        t_id = t.get("report_code") or t.get("template_id") or t.get("id")
        print(f"    模板名称: {t['name']:<20} | ID: {t_id}")
    print("=" * 55)
    print("\n💡 请将以上信息填入 .env 文件：")
    print(f"   DINGTALK_USER_ID={user_id}")
    print("   DINGTALK_TEMPLATE_ID=<选择上方对应模板的 ID>")


if __name__ == "__main__":
    phone = sys.argv[1] if len(sys.argv) > 1 else None
    fetch_ids(phone)
