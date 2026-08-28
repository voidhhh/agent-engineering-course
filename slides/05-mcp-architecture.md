---
marp: true
title: MCP 架构
---

# MCP 架构

标准化能力交换，不替代 Agent Loop

---

## 三个角色

Host 管用户体验与策略；Client 维护到某个 Server 的协议连接；Server 暴露能力。

一个 Host 可以持有多个 Client。

---

## 协议骨架

生命周期初始化 → 能力协商 → 列表/读取/调用 → 通知 → 关闭

底层消息使用 JSON-RPC 语义。

---

## 原语

- Tools：可调用动作
- Resources：可读取上下文
- Prompts：可复用提示模板

暴露资源不意味着自动可信。

---

## 实验

抓取初始化与一次工具调用，标注请求 ID、能力和错误路径。
