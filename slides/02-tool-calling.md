---
marp: true
title: Tool Calling
---

# Tool Calling

结构化意图，不是远程执行魔法

---

## 一次调用的闭环

工具模式 → 模型选择 → 参数生成 → 宿主校验 → 执行 → 结果回送 → 继续/停止

每一步都可能失败，且责任层不同。

---

## Schema 是接口

- 名称稳定、描述可判别
- 参数尽量小而强约束
- 枚举、必填、格式、范围
- 业务校验仍在可信代码中

---

## 典型失败

未知工具、JSON 无效、字段遗漏、业务越界、调用 ID 丢失、工具结果未关联。

问题：参数通过 JSON Schema 后，为什么仍可能不安全？

---

## DeepSeek 真实接口映射

- 内部 Schema → OpenAI 兼容 Function Tool
- `tool_choice`: auto / required
- Tool Call JSON 仍需宿主验证
- thinking + tools 回传 reasoning state
- 旧 model alias 不进入 2026 课程基线

---

## 实验

先用 Fake Client 验证 Adapter，再显式启用 DeepSeek Live Test；两层证据不能互相替代。
