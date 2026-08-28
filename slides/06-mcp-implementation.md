---
marp: true
title: MCP 实现
---

# MCP 实现

把函数变成可发现、可调用、可隔离的能力

---

## 两种传输

stdio：本地进程、生命周期简单、日志不能污染 stdout。

Streamable HTTP：远程部署、认证与会话更复杂。

---

## Server 责任

输入校验、业务授权、错误映射、资源界限、取消/超时、敏感数据处理。

## Client 责任

连接生命周期、能力缓存、超时、调用关联、用户审批。

---

## 失效演练

Server 输出调试文本到 stdout 会怎样？版本不兼容如何暴露？远程连接断开后调用是否安全重试？

---

## MCP 调用自研应用

REST：Adapter → loopback API

Qt：Adapter → 控制 API → Signal → GUI 主线程

CLI：Adapter → 参数数组 + JSON stdin/stdout

---

## 实验

实现任务 MCP Server；再让 MCP 分别调用 REST、Qt 与 CLI 自研软件。
