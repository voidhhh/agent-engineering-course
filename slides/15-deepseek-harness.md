---
marp: true
title: DeepSeek Harness
---

# DeepSeek Harness / Cordis

Everything is a Plugin 的收益与代价

---

## Cordis

Service：能力依赖

Event：解耦通知

Effect：可清理副作用

---

## 生命周期

注册 → 解析依赖 → 激活 → 处理事件 → 卸载清理

可插拔的难点是顺序、冲突和回滚。

---

## 权限 Hook

在执行前基于工具、参数、身份、Session、风险与审批做可信决定。

---

## 实验

Tool Plugin + Permission Hook；重复安装/卸载后监听器与服务数保持稳定。
