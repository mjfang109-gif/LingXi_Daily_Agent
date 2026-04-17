"""
节假日数据自动更新调度器

功能：
- 在 Agent 启动时自动检查是否需要更新节假日数据
- 每年12月自动同步下一年的数据
- 完全自动化，无需人工干预

使用方式：
在 agent/main.py 的启动流程中调用 check_and_update_holidays()
"""
import json
import os
from datetime import datetime

from common.config_loader import Config
from common.logger import get_logger

logger = get_logger("HolidayAutoUpdate")


def check_and_update_holidays() -> bool:
    """
    检查并自动更新节假日数据
    
    策略：
    1. 检查本地 holiday.json 是否包含明年的数据
    2. 如果不包含，自动调用同步工具更新
    3. 如果文件不存在，创建默认数据
    
    Returns:
        是否成功（False 不影响主流程，仅记录警告）
    """
    try:
        # 获取配置文件中的路径
        holiday_file = Config.get("paths.holiday_file", "holiday.json")
                
        # 如果是相对路径，转换为项目根目录的绝对路径
        if not os.path.isabs(holiday_file):
            import sys
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            holiday_file = os.path.join(project_root, holiday_file)
                
        # 如果是相对路径，转换为项目根目录的绝对路径
        if not os.path.isabs(holiday_file):
            import sys
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            holiday_file = os.path.join(project_root, holiday_file)
        
        current_year = datetime.now().year
        next_year = current_year + 1
        
        logger.info(f"📅 检查节假日数据完整性 (当前年份: {current_year}, 下一年: {next_year})")
        
        # 检查文件是否存在
        if not os.path.exists(holiday_file):
            logger.warning(f"⚠️  节假日文件不存在: {holiday_file}")
            logger.info("💡 建议运行: python tools/sync_holidays.py")
            return False
        
        # 加载现有数据
        try:
            with open(holiday_file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except Exception as e:
            logger.error(f"❌ 加载节假日文件失败: {e}")
            return False
        
        # 检查是否包含明年的数据
        next_year_prefix = f"{next_year}-"
        has_next_year_data = any(date.startswith(next_year_prefix) for date in existing_data.keys())
        
        if has_next_year_data:
            logger.info(f"✅ 节假日数据完整，已包含 {next_year} 年数据")
            return True
        
        # 需要更新
        logger.warning(f"⚠️  缺少 {next_year} 年节假日数据，准备自动同步...")
        
        # 调用同步工具
        try:
            from tools.sync_holidays import sync_holidays
            
            success = sync_holidays(
                years=[current_year, next_year],
                file_path=holiday_file,
                force=False  # 增量更新，保留历史数据
            )
            
            if success:
                logger.info(f"✅ 自动同步成功！已添加 {next_year} 年数据")
                return True
            else:
                logger.error(f"❌ 自动同步失败，请手动运行: python tools/sync_holidays.py")
                return False
                
        except ImportError:
            logger.error("❌ 无法导入同步工具，请确保 tools/sync_holidays.py 存在")
            return False
        except Exception as e:
            logger.error(f"❌ 自动同步异常: {e}", exc_info=True)
            return False
    
    except Exception as e:
        logger.error(f"❌ 检查节假日数据失败: {e}", exc_info=True)
        # 不阻断主流程，返回 False 让系统使用降级逻辑
        return False


def get_holiday_stats() -> dict:
    """
    获取节假日数据统计信息
    
    Returns:
        统计信息字典
    """
    try:
        holiday_file = Config.get("paths.holiday_file", "holiday.json")
        
        # 如果是相对路径，转换为项目根目录的绝对路径
        if not os.path.isabs(holiday_file):
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            holiday_file = os.path.join(project_root, holiday_file)
        
        if not os.path.exists(holiday_file):
            return {"error": "文件不存在"}
        
        with open(holiday_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 按年份统计
        year_stats = {}
        for date_str, info in data.items():
            year = date_str[:4]
            if year not in year_stats:
                year_stats[year] = {"total": 0, "holidays": 0, "workdays": 0}
            
            year_stats[year]["total"] += 1
            if info.get("isOffDay"):
                year_stats[year]["holidays"] += 1
            else:
                year_stats[year]["workdays"] += 1
        
        return {
            "file": holiday_file,
            "total_records": len(data),
            "years_covered": sorted(year_stats.keys()),
            "year_details": year_stats,
        }
    
    except Exception as e:
        return {"error": str(e)}
