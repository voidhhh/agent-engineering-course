# 第 8 讲：Agent Framework 与编排

## 学习目标

理解框架抽象如何映射到手写 Loop，并在单 Agent、Agent-as-Tool 与 Handoff 之间做选择。

## 1. 为什么此时才引入框架

掌握手写 Loop 后，框架中的 Agent、Runner、Session、Tool、Guardrail 和 Trace 都能落到具体机制。框架的价值是减少样板、统一生命周期和提供集成，而不是隐藏基础责任。

## 2. 核心抽象映射

Agent 通常组合模型、指令、工具和输出约束；Runner 驱动循环；Session 保存历史；Guardrail 检查输入或输出；Handoff 把控制权交给另一个 Agent；Agent-as-Tool 让主 Agent保留控制权并调用专家能力。

框架 Context 往往有两个含义：宿主代码可见的依赖对象，以及模型可见的 Token。混淆两者会导致把密钥或内部对象误放进模型上下文。

## 3. 编排选择

固定步骤优先普通代码或 Workflow；语义路由可用一个路由 Agent；专家只需返回结果时用 Agent-as-Tool；专家需要接管对话或拥有独立状态时再用 Handoff。多 Agent 会引入额外 Token、状态同步、权限和评测成本。

## 4. HITL 与持久运行

Human-in-the-loop 的关键是暂停后可序列化状态，以及审批结果与原调用精确绑定。长等待不能依赖进程内 Future；应保存 Run State，由外部事件恢复。框架若支持 durable execution，也要验证其事务和幂等语义。

## 5. Trace

Trace 应包含模型生成、工具调用、Handoff、Guardrail 和自定义事件。Trace 不是日志堆积，而是能重建一次运行因果链的结构化证据。

## 实验

使用 OpenAI Agents SDK 重构第 3 讲任务，并完成三组对照：单 Agent；规划 Agent 调用执行 Agent；Handoff 给执行 Agent。比较步数、上下文、Trace 和错误恢复复杂度。
