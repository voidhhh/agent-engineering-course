---
marp: true
title: Agent Skills
---

# Agent Skills

把程序性知识组织为按需加载的能力包

---

## 三层披露

1. `name + description`：始终可见，用于触发
2. `SKILL.md`：触发后读取核心流程
3. `scripts/references/assets`：任务需要时读取或执行

---

## 设计规则

- 描述同时说明“做什么、何时用”
- SKILL.md 简洁、使用祈使式
- 易错步骤降低自由度
- 详细知识只保留一个来源
- 脚本必须真实运行验证

---

## Skill ≠ Tool

Tool 提供动作接口；Skill 教 Agent 何时、按何顺序、用哪些约束完成一类任务。Skill 可以调用多个 Tool。

---

## 实验

实现 `research-brief`，测试应触发、不应触发、缺资料与格式校验四类 Case。
