"""
节假日数据自动同步工具

功能：
1. 从在线 API 获取最新节假日数据
2. 自动更新本地 holiday.json 文件
3. 支持增量更新（只添加新年份数据）

用法：
    python tools/sync_holidays.py              # 同步当前年份和下一年
    python tools/sync_holidays.py --year 2027  # 同步指定年份
    python tools/sync_holidays.py --force      # 强制覆盖现有数据
"""
import argparse
import json
import os
import sys
from datetime import datetime

import requests

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.logger import get_logger, setup_logging

setup_logging()
logger = get_logger("HolidaySync")

# 节假日 API（使用多个备用源）
HOLIDAY_API_URLS = [
    # 主用：timor.tech（免费稳定）
    "https://timor.tech/api/holiday/year/{year}",
]


def fetch_holiday_data(year: int) -> dict:
    """
    从在线 API 获取指定年份的节假日数据
    
    Args:
        year: 年份
        
    Returns:
        节假日数据字典，格式与 holiday.json 一致
    """
    logger.info(f"🌐 正在获取 {year} 年节假日数据...")
    
    # 尝试多个 API 源
    for api_url_template in HOLIDAY_API_URLS:
        try:
            url = api_url_template.format(year=year)
            logger.debug(f"   尝试 API: {url}")
            
            # 添加请求头，模拟浏览器请求（避免403）
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
            
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            
            data = resp.json()
            
            # 根据不同 API 的返回格式进行解析
            if "timor.tech" in api_url_template:
                # timor.tech 格式
                if data.get("code") != 0:
                    logger.warning(f"   ❌ API 返回错误: {data.get('msg', '未知错误')}")
                    continue
                            
                holidays = {}
                holiday_list = data.get("holiday", {})
                            
                for date_str, info in holiday_list.items():
                    # API 返回的日期格式可能是 "01-01" 或 "2026-01-01"
                    try:
                        # 尝试完整格式 YYYY-MM-DD
                        if len(date_str) == 10 and '-' in date_str:
                            dt = datetime.strptime(date_str, "%Y-%m-%d")
                        # 处理短格式 MM-DD（需要补全年份）
                        elif len(date_str) == 5 and '-' in date_str:
                            dt = datetime.strptime(f"{year}-{date_str}", "%Y-%m-%d")
                        else:
                            logger.warning(f"   ⚠️  无法解析日期格式: '{date_str}'")
                            continue
                        
                        normalized_date = dt.strftime("%Y-%m-%d")
                                    
                        holidays[normalized_date] = {
                            "date": normalized_date,
                            "name": info.get("name", "未知节日"),
                            "isOffDay": info.get("holiday", False),  # holiday=true 表示休息日
                        }
                    except ValueError as e:
                        logger.warning(f"   ⚠️  日期解析失败: '{date_str}', 错误: {e}")
                        continue
                            
                logger.info(f"✅ 成功获取 {year} 年数据（timor.tech），共 {len(holidays)} 条记录")
                return holidays
            
        except Exception as e:
            logger.warning(f"   ⚠️ API 请求失败: {e}")
            continue
    
    # 所有 API 都失败
    logger.error(f"❌ 所有 API 源均无法获取 {year} 年数据")
    return {}


def load_existing_holidays(file_path: str) -> dict:
    """加载现有的节假日数据"""
    if not os.path.exists(file_path):
        logger.info("📄 本地文件不存在，将创建新文件")
        return {}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"📂 已加载本地数据，共 {len(data)} 条记录")
        return data
    except Exception as e:
        logger.error(f"❌ 加载本地文件失败: {e}")
        return {}


def merge_holidays(existing: dict, new_data: dict, force: bool = False) -> dict:
    """
    合并节假日数据
    
    Args:
        existing: 现有数据
        new_data: 新数据
        force: 是否强制覆盖
        
    Returns:
        合并后的数据
    """
    if force:
        logger.warning("⚠️  强制覆盖模式：将替换所有现有数据")
        merged = new_data.copy()
    else:
        # 增量更新：只添加不存在的日期
        merged = existing.copy()
        added_count = 0
        
        for date_str, info in new_data.items():
            if date_str not in merged:
                merged[date_str] = info
                added_count += 1
            else:
                logger.debug(f"⏭️  跳过已存在的日期: {date_str}")
        
        logger.info(f"📊 新增 {added_count} 条记录，保留 {len(existing) - added_count} 条原有记录")
    
    # 按日期排序
    sorted_holidays = dict(sorted(merged.items()))
    return sorted_holidays


def save_holidays(file_path: str, data: dict) -> bool:
    """保存节假日数据到文件"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 已保存到 {file_path}，共 {len(data)} 条记录")
        return True
        
    except Exception as e:
        logger.error(f"❌ 保存文件失败: {e}")
        return False


def sync_holidays(years: list = None, file_path: str = None, force: bool = False) -> bool:
    """
    同步节假日数据
    
    Args:
        years: 要同步的年份列表，默认为当前年和下一年
        file_path: 输出文件路径
        force: 是否强制覆盖
        
    Returns:
        是否成功
    """
    # 默认参数
    if years is None:
        current_year = datetime.now().year
        years = [current_year, current_year + 1]
        logger.info(f"📅 默认同步年份: {years}")
    
    if file_path is None:
        # 使用配置文件中的路径，或默认路径
        from common.config_loader import Config
        file_path = Config.get("paths.holiday_file", "holiday.json")
        
        # 如果是相对路径，转换为项目根目录的绝对路径
        if not os.path.isabs(file_path):
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(project_root, file_path)
    
    logger.info("=" * 60)
    logger.info("  节假日数据同步工具")
    logger.info("=" * 60)
    
    # 加载现有数据
    existing_data = load_existing_holidays(file_path)
    
    # 获取每年的数据并合并
    all_new_data = {}
    success_count = 0
    
    for year in years:
        year_data = fetch_holiday_data(year)
        if year_data:
            all_new_data.update(year_data)
            success_count += 1
    
    if success_count == 0:
        logger.error("❌ 未能获取任何年份的数据，同步失败")
        return False
    
    # 合并数据
    merged_data = merge_holidays(existing_data, all_new_data, force)
    
    # 保存文件
    if save_holidays(file_path, merged_data):
        logger.info("=" * 60)
        logger.info("✅ 同步完成！")
        logger.info(f"   总记录数: {len(merged_data)}")
        logger.info(f"   涵盖年份: {sorted(set(d['date'][:4] for d in merged_data.values()))}")
        logger.info("=" * 60)
        return True
    else:
        logger.error("❌ 同步失败")
        return False


def main():
    parser = argparse.ArgumentParser(description="节假日数据自动同步工具")
    parser.add_argument(
        "--year", 
        type=int, 
        nargs="+",
        help="要同步的年份（可指定多个），默认为当前年和下一年"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default=None,
        help="输出文件路径（默认使用 config.yaml 配置）"
    )
    parser.add_argument(
        "--force", 
        action="store_true",
        help="强制覆盖现有数据（默认增量更新）"
    )
    
    args = parser.parse_args()
    
    success = sync_holidays(
        years=args.year,
        file_path=args.output,
        force=args.force
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
