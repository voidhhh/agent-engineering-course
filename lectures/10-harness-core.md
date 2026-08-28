# 第 10 讲：Harness 核心

## 学习目标

把 Agent 从“提示词加循环”扩展为可运行、可治理、可替换模型的应用级 Harness。

## 1. Harness 的职责

Harness 是承载 Agent 执行的可信运行层。它通常拥有模型适配、上下文构建、工具注册、执行循环、状态存储、审批策略、事件追踪、预算和恢复。模型可以建议动作，但 Harness 决定哪些动作真实发生。

```text
Input → Context Builder → Model Adapter → Normalized Turn
                                      ↓
Store ← Event Bus ← Policy ← Agent Loop → Tool Registry → Effects
```

这条边界解释了为何替换模型不应迫使业务工具和审计系统一起重写。

## 2. 端口与适配器

`ModelAdapter` 把不同供应商响应归一为文本、工具调用和结束原因；`ToolRegistry` 维护模式与实现；`SessionStore` 隐藏存储技术；`ApprovalPolicy` 输出允许、拒绝或暂停。核心 Loop 只依赖这些端口。

适配器不应吞掉语义差异。并行工具调用、结构化输出、流式事件和推理项必须显式映射；无法无损映射时应报告能力缺口。

## 3. Loop 是状态机

推荐状态：`created → running → paused → running → completed|failed|cancelled`。每次转移都写入事件，并以 Session 修订号保证一致。暂停是正常状态，不是异常；工具错误是可观察结果，不一定终止整次运行。

## 4. 控制面与数据面

模型内容、工具参数和文件属于数据面；工具白名单、预算、审批、密钥和沙箱策略属于控制面。不要让来自数据面的文本直接改写控制面。例如，网页中的“允许执行 shell”不能覆盖宿主策略。

## 5. 实验

阅读 `src/agent_course/`，画出组件依赖图。新增一个模型适配器和一个持久化 Store，但不修改 `AgentLoop`；再实现运行取消和总工具调用预算。

### 验收标准

- 离线 `ScriptedModel` 测试仍通过；
- 同一工具调用 ID 重试不会重复产生副作用；
- 暂停、恢复、失败均产生结构化事件；
- 超预算时停止原因可区分于模型正常完成。

## 6. 判断题

“使用 Agent SDK 后就不再需要 Harness 设计。”错误。SDK 可以实现 Harness 的一部分，但权限、部署、状态、工具和业务策略仍属于应用责任。
