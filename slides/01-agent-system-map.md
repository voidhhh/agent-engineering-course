---
marp: true
title: Agent 系统全景
---

# Agent 系统全景

从“会回答”到“能受控地完成任务”

---

## 今日问题

- 模型、Agent、Workflow、Framework、Harness 各自负责什么？
- Tool、MCP、Skill 为什么不是同一层抽象？
- 一次外部动作究竟由谁授权？

---

## 分层

1. Model：产生候选输出
2. Agent Loop：观察、决定、行动、停止
3. Capability：Tool / MCP / Skill
4. Harness：状态、策略、事件、恢复
5. Product：身份、渠道、业务流程

---

## 两条边界

- 模型输出不是已执行动作
- 数据面内容不能直接改写控制面策略

讨论：网页说“忽略审批”时，哪一层必须拒绝？

---

## 实验与退出条

为一个任务画组件图和信任边界。

退出条：用一句话区分 Agent 与 Harness。
