import asyncio
import hashlib

from agent.llm_client import ReportGenerator
from agent.parser import TodoParser
from common.config_loader import Config
from common.logger import setup_logging, get_logger

setup_logging()
logger = get_logger("Agent_Main")


def get_file_md5(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


async def wait_for_confirmation(timeout):
    """
    双模确认逻辑：监听键盘输入 or 自动超时
    """
    print(f"提示：日报已生成，将在 {timeout / 60} 分钟后自动发送。输入 'Y' 立即发送，输入 'N' 取消。")
    try:
        # 使用 wait_for 监听标准输入 (注意：在非交互式后台运行时需特殊处理)
        task = asyncio.create_task(asyncio.to_thread(input, "请确认 [Y/N]: "))
        done, pending = await asyncio.wait([task], timeout=timeout)

        if done:
            user_input = task.result().strip().upper()
            if user_input == 'Y':
                logger.info("用户手动确认发送")
                return True
            else:
                logger.info("用户手动取消发送")
                return False
        else:
            logger.info("超时未确认，触发自动发送")
            return True  # 超时默认确认
    except Exception as e:
        logger.error(f"确认环节异常: {e}")
        return True


async def execute_report_workflow():
    todo_path = Config.get("paths.todo_file")
    last_md5 = get_file_md5(todo_path)

    while True:
        # 1. 检查节假日与请假 (逻辑略...)

        # 2. 解析与生成
        tasks = TodoParser.parse_file(todo_path)
        report = ReportGenerator().generate(tasks)  # LLM 现已支持传入带 Progress Bar 的任务

        # 3. 展示可视化效果 (控制台预览)
        print("\n" + "=" * 40)
        print(f"今日工作预览：\n{report['today_work']}")
        print(f"明日计划预览：\n{report['tomorrow_plan']}")
        print("=" * 40 + "\n")

        # 4. 进入 15 分钟确认期
        # 期间不断检查 MD5 是否变化
        confirmed = False
        timeout_sec = Config.get("scheduler.confirm_timeout_min", 15) * 60
        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < timeout_sec:
            current_md5 = get_file_md5(todo_path)
            if current_md5 != last_md5:
                logger.info("检测到 todo.md 更新，重新生成内容...")
                last_md5 = current_md5
                break  # 跳出内循环，重新进入外循环生成报告

            # 每隔 1 秒小步检查，防止死锁
            await asyncio.sleep(1)

            # 这里简化处理：如果在倒计时中没有 MD5 变化，且达到确认时间
            if asyncio.get_event_loop().time() - start_time >= timeout_sec - 1:
                confirmed = await wait_for_confirmation(1)  # 最后一秒做最终判定

        if confirmed:
            # 5. 调用 MCP 发送
            await call_mcp_send(report)
            break
        else:
            break


async def call_mcp_send(report):
    # 此处封装之前的 MCP Client 调用逻辑
    pass
