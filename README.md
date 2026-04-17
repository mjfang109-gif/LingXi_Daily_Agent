# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
</p>

---

## 📋 项目简介

LingXi Daily Agent 是一款面向企业办公场景的智能化日报助手，采用 **Agent 架构设计**，将复杂的工作日报生成流程拆解为消息监听、任务解析、AI 润色、双模确认、消息推送等多个独立模块，通过 MCP 解耦底层 API 调用。

### 核心特性

| 特性 | 说明 |
|------|------|
| 📱 **纯消息驱动** | 无需文件，完全通过钉钉消息添加任务 |
| 🤖 **Agent 编排** | 大脑层负责工作流编排，不直接调用底层 API |
| 🧠 **AI 智能润色** | 调用大模型将口语化任务转换为专业职场表述 |
| 📱 **钉钉深度集成** | WebSocket 长连接实时接收消息，卡片消息推送 |
| 🔄 **热更新机制** | 15 分钟确认期内发送新任务，自动重新生成 |
| 📅 **节假日智能跳过** | 读取配置判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |

---

## 🏗 系统架构

### 整体架构图

```mermaid
flowchart TB
    subgraph 用户层["�ользователь 用户层"]
        direction LR
        用户[钉钉用户]
        手机[手机端]
        电脑[PC端]
        用户 --> 手机
        用户 --> 电脑
    end

    subgraph Agent层["🤖 Agent 大脑层"]
        direction TB
        main["main.py<br/>主工作流编排"]
        parser["parser.py<br/>任务解析器"]
        llm["llm_client.py<br/>LLM 润色引擎"]
        chat["chat_engine.py<br/>AI 聊天引擎"]
        dt["dingtalk_client.py<br/>钉钉客户端"]
        
        main -.-> parser
        main -.-> llm
        main -.-> chat
        main -.-> dt
    end

    subgraph MCP层["🔌 MCP 服务层"]
        direction TB
        mcp["server.py<br/>MCP 路由器"]
        dtapi["dingtalk_api.py<br/>钉钉 API"]
        dtmsg["dingtalk_message.py<br/>消息服务"]
        holiday["holiday_api.py<br/>节假日查询"]
    end

    subgraph 外部服务["☁️ 外部服务"]
        direction LR
        DT["钉钉开放平台"]
        LLM["大模型 API"]
        Local["本地存储"]
        
        DT --- DT1["Open API"]
        DT --- DT2["Stream WebSocket"]
        DT --- DT3["日志服务"]
    end

    subgraph 存储层["💾 存储层"]
        UserStore["user_store.py<br/>用户会话存储"]
        Config["config_loader.py<br/>配置管理"]
        Logger["logger.py<br/>日志模块"]
    end

    用户 -->|"发送任务消息"| Agent层
    Agent层 -->|"MCP 调用"| MCP层
    MCP层 -->|"HTTP/WS"| 外部服务
    Agent层 -->|"读写"| 存储层
    
    style Agent层 fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style MCP层 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style 外部服务 fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style 存储层 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
```

### 工作流程图

```mermaid
sequenceDiagram
    participant User as 用户
    participant WebSocket as WebSocket监听
    participant Parser as 任务解析器
    participant Store as UserStore
    participant LLM as LLM引擎
    participant Preview as 预览卡片
    participant Confirm as 确认等待
    participant DT as 钉钉API
    participant Log as 钉钉日志

    User->>WebSocket: 发送任务消息<br/>"1. 修复Bug@4.17"
    WebSocket->>Parser: 解析任务
    Parser->>Store: 存储任务
    Store-->>Parser: 任务版本号
    
    Note over Store: 定时触发（每日 18:10）
    
    Store->>LLM: 获取今日+明日任务
    LLM-->>Store: 润色后的日报
    Store->>Preview: 发送预览卡片
    Preview->>User: 展示日报预览
    
    Note over Confirm: 等待 15 分钟
    
    loop 热更新检测
        User->>WebSocket: 发送新任务
        WebSocket->>Store: 更新任务
        Store->>Preview: 重新生成并发送
    end
    
    User->>Confirm: 回复 "Y" 确认
    Confirm->>DT: 提交日报
    DT->>Log: 创建工作日志
    Log-->>User: 发送成功通知
```

### 模块依赖关系

```mermaid
flowchart TB
    subgraph agent["agent/ 核心业务"]
        main["main.py"]
        parser["parser.py"]
        llm["llm_client.py"]
        chat["chat_engine.py"]
        dingtalk["dingtalk_client.py"]
    end
    
    subgraph mcp["mcp_server/ 服务层"]
        server["server.py"]
        dt_api["dingtalk_api.py"]
        dt_msg["dingtalk_message.py"]
        holiday["holiday_api.py"]
    end
    
    subgraph common["common/ 公共"]
        config["config_loader.py"]
        logger["logger.py"]
        store["user_store.py"]
    end
    
    main --> parser
    main --> llm
    main --> dingtalk
    main --> config
    main --> store
    
    dingtalk --> dt_msg
    dt_msg --> dt_api
    
    parser --> store
    llm --> config
    chat --> config
    
    server --> dt_api
    server --> dt_msg
    
    style main fill:#ff9800,color:#000
    style dingtalk fill:#ff9800,color:#000
    style dt_msg fill:#4caf50,color:#fff
    style store fill:#9c27b0,color:#fff
```

---

## 📦 项目结构

```
LingXi_Daily_Agent/
├── agent/                          # Agent 核心业务逻辑
│   ├── main.py                     # 主工作流入口
│   ├── parser.py                   # 任务解析器（解析钉钉消息）
│   ├── llm_client.py               # LLM 润色引擎
│   ├── chat_engine.py              # AI 聊天引擎（非任务消息）
│   ├── dingtalk_client.py          # 钉钉客户端（消息发送+监听）
│   └── prompts/
│       └── report_polish_prompt.txt # 日报润色提示词
│
├── mcp_server/                     # MCP 工具服务层
│   ├── server.py                   # MCP 路由器
│   └── services/
│       ├── dingtalk_api.py         # 钉钉 API 封装
│       ├── dingtalk_message.py     # 消息服务（卡片+监听）
│       ├── holiday_api.py          # 节假日查询
│       └── local_fs.py             # 本地文件服务
│
├── common/                         # 公共模块
│   ├── config_loader.py            # 配置加载
│   ├── logger.py                   # 日志模块
│   └── user_store.py               # 用户会话存储（内存）
│
├── tools/                          # 辅助工具
│   └── fetch_dingtalk_ids.py       # 初始化工具（获取 UserID/模板）
│
├── config.yaml                     # 业务配置文件
├── logging.yaml                    # 日志配置文件
├── holiday.json                    # 年度节假日配置
├── requirements.txt                # Python 依赖
├── .env.example                    # 环境变量模板
└── .env                            # 环境变量
```

---

## 🚀 快速开始

### 1. 环境要求

| 环境 | 要求 |
|------|------|
| Python | 3.10+ |
| 操作系统 | macOS / Linux / Windows |
| 钉钉 | 企业账号（需开放平台开发者权限） |
| 大模型 | OpenAI 兼容 API |

### 2. 克隆与安装

```bash
# 克隆项目
git clone <repository-url>
cd LingXi_Daily_Agent

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 环境变量配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
```

`.env` 文件配置项详解：

| 变量名 | 必填 | 说明 | 获取方式 |
|--------|:----:|------|----------|
| `DINGTALK_CLIENT_ID` | ✅ | 钉钉应用 AppKey | 见钉钉配置章节 |
| `DINGTALK_CLIENT_SECRET` | ✅ | 钉钉应用 AppSecret | 见钉钉配置章节 |
| `DINGTALK_ROBOT_CODE` | ✅ | 机器人 Code | 见钉钉配置章节 |
| `DINGTALK_USER_ID` | ✅ | **默认用户的 UserID** | 运行初始化工具获取 |
| `DINGTALK_TEMPLATE_ID` | ✅ | **默认日志模板 ID** | 运行初始化工具获取 |
| `LLM_API_KEY` | ✅ | 大模型 API Key | OpenAI 或兼容服务商后台 |
| `LLM_BASE_URL` | ✅ | API 端点地址 | 默认 `https://api.openai.com/v1` |
| `LLM_MODEL` | ✅ | 模型名称 | 如 `gpt-4o-mini`、`deepseek-chat` |

> **注意**：`DINGTALK_USER_ID` 和 `DINGTALK_TEMPLATE_ID` 是**单用户模式的配置**，也是多用户模式下的全局默认值。系统启动后会根据用户首次对话自动识别并缓存该用户对应的模板字段结构。

### 4. 获取钉钉 UserID 和模板 ID

```bash
# 运行初始化工具（需先配置 CLIENT_ID 和 CLIENT_SECRET）
python tools/fetch_dingtalk_ids.py 你的手机号
```

输出示例：

```
=======================================================
  👤 UserID：xxxxxxxxxxxx
-------------------------------------------------------
  📋 可见日志模板列表（共 2 个）:
    模板名称: 安建数科一般员工日志 | ID: template_xxx1
    模板名称: 每日日报           | ID: template_xxx2
=======================================================

💡 请将以下信息填入 .env 文件：
   DINGTALK_USER_ID=xxxxxxxxxxxx
   DINGTALK_TEMPLATE_ID=<选择模板 ID>
```

### 5. 业务配置（config.yaml）

```yaml
# 定时任务配置
scheduler:
  report_time: "18:10"          # 每天生成日报的触发时间 (HH:MM)
  confirm_timeout_min: 15       # 人工确认等待窗口（分钟）
  check_interval_sec: 10        # 任务热更新轮询间隔（秒）

# 节假日文件路径
paths:
  holiday_file: "./holiday.json"

# 钉钉业务配置（全局默认值，可被 per-user 配置覆盖）
dingtalk:
  report_field_today: "今日工作"    # 全局默认：今日工作字段名（无法从模板缓存获取时的兜底）
  report_field_tomorrow: "明日计划" # 全局默认：明日计划字段名
  report_dd_from: "report"          # 日志来源标识
  # 模板自动识别关键词：用于从用户可见模板列表中匹配日报模板
  daily_report_name_keywords:
    - "日报"
    - "每日"
    - "日志"

# 多用户配置（可选）
# users:
#   - user_id: "user001"
#     template_id: "template_abc"
#     contents:                    # 自定义字段映射（需与钉钉模板字段名一致）
#       - sort: 1
#         key: "今日工作"
#       - sort: 2
#         key: "明日计划"
```

#### AI 对话配置（llm）

```yaml
llm:
  # 用户位置信息，用于天气等问题问答
  location: "北京市"

  # 位置上下文提示词模板，{location} 会被替换为用户实际位置
  location_prompt: "你已了解用户位于「{location}」，当用户询问天气、出行、本地资讯等相关问题时，可以结合该位置给出更准确的回答。"

  # 联网搜索配置（默认启用阿里千问）
  # 支持的 provider:
  #   - qwen: 阿里千问（默认），使用 extra_body.enable_search
  #   - deepseek: DeepSeek，使用 extra_body.enable_search
  #   - moonshot: 月之暗面 Moonshot，使用 extra_body.search_options.enable
  #   - zhipu: 智谱 GLM，使用 extra_body.search_retrieval
  #   - custom: 自定义 extra_body 参数
  web_search:
    provider: "qwen"

  chat_system_prompt: |
    你现在是 LingXi 办公助理...
```

#### 配置说明

| 配置项 | 说明 |
|--------|------|
| `scheduler.*` | 定时触发和确认超时配置 |
| `dingtalk.report_field_today` | 钉钉日志内容的 **key** 字段名，对应模板中「今日工作」字段的唯一标识 |
| `dingtalk.report_field_tomorrow` | 钉钉日志内容的 **key** 字段名，对应模板中「明日计划」字段的唯一标识 |
| `dingtalk.dd_from` | 日志来源标识（用于钉钉日志接口的 `dd_from` 参数） |
| `dingtalk.daily_report_name_keywords` | **模板自动识别关键词**，Agent 会从用户可见的模板列表中查找名称包含这些关键词的模板作为日报模板 |
| `llm.location` | 用户位置信息，用于天气/出行等问题回答（如"北京市"、"上海市,上海市,中国"） |
| `llm.web_search` | 是否启用联网搜索，支持多种厂商配置 |
| `users` | 多用户配置，每个用户可使用不同的模板和字段映射 |

> **关键说明**：
> - `report_field_today` 和 `report_field_tomorrow` 必须与钉钉日志模板中定义的**字段名（key）完全一致**
> - `llm.location` 配置后，AI 在回答天气等相关问题时会自动结合该位置给出更准确的回答 |

### 6. 启动 Agent

```bash
python -m agent.main
```

启动后，Agent 将：
1. 连接钉钉 WebSocket 监听消息
2. 进入定时等待状态
3. 用户发送任务后自动处理

---

## 🛠 钉钉开放平台配置指南

### 步骤 1：创建企业应用

1. 登录 [钉钉开放平台](https://open.dingtalk.com/)
2. 进入「应用开发」→「企业内部开发」
3. 点击「创建应用」
4. 填写应用信息：
   - 应用名称：`LingXi Daily Agent`
   - 应用描述：`智能工作日报助手`
5. 创建成功后，获取 **AppKey** 和 **AppSecret**

### 步骤 2：配置机器人

1. 在应用详情页，点击「添加应用能力」→「机器人」
2. 配置机器人信息：
   - 机器人名称：`LingXi 日报助手`
   - 描述：`自动化工作日报生成与发送`
3. **关键配置**：
   - 消息接收模式：选择 **「Stream 推送（WebSocket）」**
4. 启用机器人，获取 **Robot Code**

### 步骤 3：申请权限

在应用的「权限管理」中，需要开通以下权限：

| 权限名称 | 权限码 | 用途 |
|----------|--------|------|
| 发送工作通知 | `work_notification` | 向用户发送卡片/文本消息 |
| 查询员工信息 | `ool.employee.Query` | 根据手机号查询 UserID |
| 提交日志 | `report.create` | 向钉钉提交工作日志 |
| 查询日志模板 | `report.template.listbyuserid` | 获取用户可见的日志模板 |
| 查询日志模板详情 | `report.template.getbyid` | 获取模板字段结构 |
| 查询考勤状态 | `attendance.getusergroup` | 检测用户是否请假/休息 |

### 步骤 4：发布应用

1. 在应用详情页，点击「发布」
2. 填写发布信息并提交企业审批
3. 审批通过后，可见范围内的人员即可使用

---

## 💬 使用流程

### 任务添加方式

直接在钉钉对话中发送任务消息：

```
1. 修复登录 Bug@4.17
2. 梳理微服务架构@4.17@未完成，进度60%
3. 对接支付回调@4.18
```

**格式规范**：`序号. 任务描述@日期@状态`

| 部分 | 是否必填 | 说明 | 示例 |
|------|:--------:|------|------|
| 序号 | ✅ | 支持 `.` 或 `、` | `1.` 或 `1、` |
| 任务描述 | ✅ | 工作内容 | `完成登录功能` |
| 日期 | ❌ | `MM.DD` | `@4.17` |
| 状态 | ❌ | 多种写法 | 见下表 |

**状态格式兼容**：

| 写法 | 解析结果 |
|------|----------|
| 空/省略 | ✅ 已完成 |
| `已完成` / `完成` / `100%` | ✅ 已完成 |
| `未完成` / `进行中` | ⏳ 推进中 0% |
| `进度60%` / `60%` | ⏳ 推进中 60% |
| `计划中` | 📅 计划中 |

### 自动日报生成

1. 每天到达配置时间（如 18:10）
2. 检查是否为工作日（非节假日）
3. 检查用户考勤状态（请假/休息则跳过）
4. 从内存获取任务，调用 LLM 生成日报
5. 发送预览卡片到钉钉
6. 用户确认后提交到钉钉日志

---

## 📱 消息交互示例

### 日报预览卡片

```
✨ 工作日报预览（04/16 17:50）

### 📋 今日工作
1. ✅ 完成用户登录鉴权缺陷修复，确保线上认证稳定
2. ✅ 完成代码审查，保障代码质量

### 🗓 明日计划
1. ⏳ 推进中 ▓▓▓▓▓▓░░░ 60%：持续完善微服务架构设计文档
2. 📅 计划中：对接第三方支付平台回调接口联调

---
⏱ 请在 **15 分钟**内回复 **Y** 确认立即发送，超时将自动发送。
```

### 响应指令

| 指令 | 动作 |
|------|------|
| `Y` / `是` / `确认` | 立即提交日报 |
| `N` / `否` / `取消` | 取消提交 |
| 超时 | 自动提交日报 |

### 热更新机制

在 15 分钟确认窗口期内发送新任务：
1. Agent 检测到任务版本变化
2. 重新调用 LLM 生成新版日报
3. 重新发送预览卡片，**倒计时重置**

---

## 🏷 节假日配置

编辑 `holiday.json`：

```json
{
  "2026-01-01": {"date": "2026-01-01", "name": "元旦", "isOffDay": true},
  "2026-04-04": {"date": "2026-04-04", "name": "清明节", "isOffDay": true}
}
```

- `isOffDay: true` → 跳过生成
- `isOffDay: false` → 正常生成

---

## ❓ 常见问题

### Q1: 启动报错 "缺少 DINGTALK_CLIENT_ID"

检查 `.env` 文件是否正确配置。

### Q2: 收不到钉钉消息

1. 确认机器人已开启「Stream 推送」模式
2. 确认已开通「发送工作通知」权限
3. 检查 `DINGTALK_USER_ID` 是否正确

### Q3: 大模型调用失败

- 确认 `LLM_API_KEY` 正确
- 检查网络能否访问 `LLM_BASE_URL`

### Q4: 日志提交失败

1. 确认已开通「提交日志」权限
2. 确认 `DINGTALK_TEMPLATE_ID` 与用户模板匹配

### Q5: 如何支持多用户

在 `config.yaml` 中配置 `users` 列表。

---

## 📄 许可证

MIT License