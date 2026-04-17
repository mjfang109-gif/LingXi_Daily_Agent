# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DingTalk-集成-orange?style=flat-square" alt="DingTalk">
  <img src="https://img.shields.io/badge/AI-Qwen-9cf?style=flat-square" alt="AI Model">
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
| 📅 **节假日智能跳过** | 自动同步官方数据，判断是否需要生成日报 |
| 👀 **考勤状态联动** | 自动检测请假/休息状态，静默跳过 |
| 👥 **多用户支持** | 独立会话隔离，个性化模板配置 |
| 🌐 **联网搜索** | 支持天气、资讯等实时信息查询 |

---

## 🏗 系统架构

### 整体架构图

```
# LingXi Daily Agent

> 智能工作日报生成与发送 Agent - 自动化、AI 润色、实时交互、节假日自动同步

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https/```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```
