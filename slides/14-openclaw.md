---
marp: true
title: OpenClaw
---

# OpenClaw

长驻 Gateway 改变了 Agent 的工程问题

---

## 核心边界

Channel/Client ↔ Gateway ↔ Session/Runtime ↔ Workspace/Tools

WebSocket 只负责连接，不自动解决身份和权限。

---

## 长驻系统新增问题

重连、排队、会话锁、后台任务、升级迁移、渠道身份映射。

---

## Workspace 风险

指令、Skill、Memory、文件与产物共处；便利与持久污染风险同时上升。

---

## 实验

本地 Gateway + 测试 Client；注入断线、并发和超时，验证持久状态与清理。
