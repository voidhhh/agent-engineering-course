---
marp: true
title: Hermes Agent
---

# Hermes Agent

用轨迹和文件差异验证运行时主张

---

## 追踪路径

输入 → Prompt → Model → Tool → Result → Session → Skill/Memory 写入

从一个最小任务追，不从功能列表猜。

---

## “自我改进”

重点观察 Skill、Memory、配置或工作区工件变化；不要误写成在线训练模型权重。

---

## 验证闭环

记录变更前后差异 → 禁用新增内容重跑 → 恢复后再跑 → 比较行为证据。

---

## 实验

隔离目录完成研究简报任务，标注 Loop、工具、Skill、Memory、MCP 证据位置。
