# 第 3 讲：最小 Agent Loop

## 学习目标

不使用 Agent 框架，独立实现可终止、可测试、可观察的推理—行动—观察循环。

## 1. 循环为何是 Agent 的核心

单次模型调用只能基于已知上下文回答。Agent Loop 允许模型通过行动获取新事实，再基于观察决定下一步。真正提升来自“新观察改变后续决策”，而不是简单多调用几次模型。

最小循环只需要：消息列表、模型适配器、工具注册表、最大步数和终止规则。框架会包装这些概念，但不会消除它们。

## 2. 状态机

可将运行表示为：`ready → running → paused/completed/failed`。`paused` 不是失败，而是等待外部审批或输入；`failed` 必须保存明确原因；`completed` 必须对应可验证的终止事件。

每轮顺序为：构造上下文、调用模型、记录响应、处理工具、写入观察、检查预算。最大步数是宿主不变量，模型不能自行提高。超时和费用预算也应独立于自然语言指令。

## 3. 模型适配器

不同提供商返回不同对象。Harness 应尽早归一化为
`ModelTurn(content, reasoning, tool_calls, finish_reason, usage)`。后续 Loop 不应散布
提供商字段，否则更换模型会修改策略、Trace 和测试。Trace 记录结构化 Token 用量，
但不默认记录 reasoning 正文。

离线 `ScriptedModel` 是重要教学工具。它允许固定每一轮返回，准确测试工具调用、暂停、错误和步数预算，而不受模型随机性和网络影响。

真实 API Adapter 还承担协议翻译，而不是只替换 URL：工具 Schema 形状、Tool Call
参数、结束原因、Token 用量和中间推理字段都需要归一化。DeepSeek thinking 模式在
带工具的多轮请求中要求回传 `reasoning_content`；核心 Loop 将其保存为通用
`ModelTurn.reasoning`，由 Adapter 再映射回提供商字段。

课程采用三层测试：`ScriptedModel` 验证 Loop；Fake Client 验证 Adapter；显式 Live
Test 验证当前服务。只有第三层需要 Key、网络和费用，且其随机结果不能成为核心 CI
唯一通过条件。

## 4. 终止条件

终止至少包括：模型产生最终答案；达到步数/时间/费用预算；不可恢复的提供商错误；用户取消；策略拒绝且任务无法继续。只检查“模型没有工具调用”还不够，还应验证输出是否符合要求。

## 5. 失效模式

无限循环通常来自重复失败、模型看不到规范化错误、调用结果未正确关联或没有预算。幽灵完成来自只返回 HTTP 200，却没有持久化最终状态。重启丢失来自只在内存保存消息而没有 Checkpoint。

## 实验

阅读 `src/agent_course/loop.py`，用 ScriptedModel 构造“调用加法工具—观察结果—给出答案”。随后构造永远调用 `list_tasks` 的模型，验证第二步后以预算错误结束。

再阅读 `src/agent_course/deepseek.py`，运行[实验 01B](../labs/01b-deepseek-api.md)，
证明更换模型提供商不需要修改 `AgentLoop`。

## 反思

框架可以减少样板代码，但如果学习者无法指出状态转换、预算检查和工具结果进入下一轮的位置，就还没有掌握 Agent Loop。
