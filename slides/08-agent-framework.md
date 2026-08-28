---
marp: true
title: Agent Framework
---

# Agent Framework

理解抽象后再享受抽象

---

## 映射

Agent = 模型 + 指令 + 工具 + 输出约束

Runner = Loop；Session = 状态；Guardrail = 检查；Trace = 因果记录。

---

## 编排选择

固定步骤用代码；专家只提供结果用 Agent-as-Tool；专家接管分支时用 Handoff。

默认从一个 Agent 开始。

---

## OpenAI 路径选择

需要自己控制 Loop：Responses API。

需要 SDK 管循环、Session、Trace、Guardrail、可恢复审批：Agents SDK。

---

## 实验

用 SDK 重构手写 Loop，比较单 Agent、Agent-as-Tool 与 Handoff 的轨迹。
