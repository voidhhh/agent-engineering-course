---
marp: true
title: Harness 核心
---

# Harness 核心

可信运行层决定真实世界发生什么

---

## 组件

Model Adapter、Context Builder、Agent Loop、Tool Registry、Policy、Store、Event Bus、Budget。

---

## 状态机

`created → running → paused → running → completed | failed | cancelled`

暂停是正常终点之一，不是异常。

---

## 控制面 / 数据面

控制面：权限、预算、审批、密钥。

数据面：消息、工具参数、文件、网页。

数据面不得自我授权。

---

## 实验

替换 Model Adapter 与 Store 而不修改 Loop；新增取消和调用预算。
