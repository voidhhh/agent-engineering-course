---
marp: true
title: Context Session Memory
---

# Context / Session / Memory

别把所有状态都叫“记忆”

---

## 四问

Context：本次看什么？

Session：这段交互是谁的？

Memory：以后召回什么？

Checkpoint：中断后从哪里继续？

---

## Context Builder

来源 → 信任分级 → 去重 → 优先级 → 压缩 → 预算 → 模型输入

摘要必须保留未完成承诺和审批状态。

---

## Memory 生命周期

候选、验证、写入、召回、使用、过期/删除。

“模型说记住了”不等于存储提交。

---

## 实验

SQLite Session + 修订号；对比全量、滑窗、摘要三种上下文策略。
