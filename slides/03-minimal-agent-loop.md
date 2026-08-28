---
marp: true
title: 最小 Agent Loop
---

# 最小 Agent Loop

让每次继续与停止都有依据

---

## 状态转移

模型返回文本 → 完成

模型返回工具调用 → 执行并回送 → 再次调用模型

越过步数预算 → 失败

---

## 必要不变量

- 工具结果绑定原调用 ID
- 每步都有预算
- Provider 错误归一化
- 历史顺序不可破坏
- 完成只由明确终止条件触发

---

## 离线测试为何关键

用 `ScriptedModel` 固定模型输出，才能单独验证 Loop，而不是把随机模型行为误判为运行时 Bug。

---

## 三层模型测试

1. ScriptedModel：Loop 状态与预算
2. Fake Client：Provider Adapter 映射
3. DeepSeek Live：当前服务兼容性与用量

只有第三层需要 Key、网络和费用。

---

## 实验

跑通离线两步工具调用，再用同一 Loop 接入 `DeepSeekChatAdapter`。
