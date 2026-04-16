# LingXi Daily Agent

> 自动化工作日报生成 & 发送 Agent，支持钉钉机器人单聊卡片消息预览 + 双模确认 + 热更新

---

## 功能矩阵

| # | 模块 | 状态 | 说明 |
|---|------|:----:|------|
| 1 | 任务格式规范 | ✅ | `序号. 描述@日期@状态`，兼容 `.` 和 `、` |
| 2 | 字段容错解析 | ✅ | 状态/日期均可省略，省略状态默认已完成，省略日期归入今日 |
| 3 | 配置化日历 | ✅ | 统一走 `config.yaml` + `holiday.json` |
| 4 | 节假日阻断 | ✅ | 读取 `holiday.json`，含 `(休)` 标记则阻断 |
| 5 | 钉钉考勤状态 | ✅ | 接口预留，请假自动静默退出 |
| 6 | AI 专业级润色 | ✅ | GPT JSON 模式，按「今日/明日」格式化输出 |
| 7 | 双模确认机制 | ✅ | 卡片预览 → 15min 倒计时 → 手动 Y/N 或超时自动发 |
| 8 | 文本进度条 | ✅ | `▓▓▓░░` 格式，跨天/带进度任务自动生成 |
| 9 | 数据可视化卡片 | ✅ | Markdown 表格 + 状态 Emoji（✅⏳📅） |
| 10 | MD5 热更新 | ✅ | 倒计时期间 `todo.md` 变动 → 重新生成 + 重置倒计时 |
| 11 | Agent 定位 | ✅ | Agent 只编排，不碰底层 API |
| 12 | MCP 解耦调用 | ✅ | `subprocess` 唤起 `mcp_server`，支持 FastMCP + CLI 两种模式 |

---

## 项目结构

```
LingXi_Daily_Agent/
├── agent/
│   ├── main.py              # 主工作流（双模确认 + 热更新 + MCP 调度）
│   ├── dingtalk_client.py   # 钉钉单聊卡片消息发送（核心）
│   ├── llm_client.py        # LLM 润色引擎
│   ├── parser.py            # todo.md 解析器
│   ├── scheduler.py         # 定时任务包装器
│   └── prompts/
│       └── report_polish_prompt.txt
├── mcp_server/
│   ├── server.py            # MCP 工具路由（FastMCP + CLI 双模式）
│   └── services/
│       ├── dingtalk_api.py  # 钉钉 API 封装
│       ├── holiday_api.py   # 节假日在线查询
│       └── local_fs.py      # 本地节假日文件读取
├── common/
│   ├── config_loader.py     # 统一配置（.env + config.yaml）
│   └── logger.py            # 日志初始化
├── tools/
│   └── fetch_dingtalk_ids.py  # 一键获取 UserID 和模板列表
├── todo.md                  # 任务清单（每日编辑）
├── holiday.json             # 年度节假日配置
├── config.yaml              # 业务配置
├── logging.yaml             # 日志配置
├── requirements.txt
└── .env.example             # 环境变量模板
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入钉钉和 LLM 凭证
```

**必填项：**

| 变量名 | 说明 |
|--------|------|
| `DINGTALK_CLIENT_ID` | 钉钉应用 AppKey |
| `DINGTALK_CLIENT_SECRET` | 钉钉应用 AppSecret |
| `DINGTALK_ROBOT_CODE` | 机器人 Code（在开放平台机器人配置中获取） |
| `DINGTALK_USER_ID` | 接收预览消息的用户 UserID |
| `LLM_API_KEY` | 大模型 API Key |
| `LLM_BASE_URL` | 大模型 Base URL（默认 OpenAI） |
| `LLM_MODEL` | 模型名称（如 `gpt-4o-mini`） |

### 3. 获取钉钉 UserID（首次）

```bash
python tools/fetch_dingtalk_ids.py 138xxxxxxxx
```

### 4. 编写今日任务

编辑 `todo.md`，格式示例：

```
1. 修复登录 Bug@4.16
2. 梳理微服务架构@4.16@未完成，进度60%
3. 对接支付回调@4.17@未完成
```

### 5. 启动 Agent

```bash
python -m agent.main
```

---

## 卡片消息效果

Agent 在每日 `17:50`（可配）触发，通过钉钉机器人向你单聊发送如下**普通卡片**：

```
✨ 工作日报预览（04/16 17:50）

### 📋 今日工作
1. ✅ 完成用户登录鉴权缺陷修复，确保线上认证稳定性
2. ✅ 完成代码审查，保障代码质量与规范一致性

### 🗓 明日计划
1. ⏳ 推进中 ▓▓▓▓▓▓░░░░ 60%：持续完善微服务架构设计文档
2. 📅 计划中：对接第三方支付平台回调接口联调

### 📊 任务摘要
| 任务状态 | 数量 |
|:---:|:---:|
| ✅ 已完成 | 2 |
| ⏳ 推进中 | 1 |
| 📅 计划中 | 1 |

---
⏱ 请在 **15 分钟**内回复 **Y** 确认立即发送，超时将自动发送。
```

---

## 热更新机制

在 15 分钟等待窗口内，若你修改并保存了 `todo.md`：

1. Agent 检测到文件 MD5 变化
2. 自动重新调用 LLM 生成新版日报
3. 重新发送预览卡片，**倒计时重置**

---

## MCP 解耦架构

```
agent/main.py          （大脑：编排工作流，不碰底层 API）
      │
      │  asyncio.create_subprocess_exec
      ▼
mcp_server/server.py   （工具层：CLI 子进程模式接收 JSON payload）
      │
      ▼
DingTalkService        （底层：钉钉 API 真正调用）
```
