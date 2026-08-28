# 第 2 讲：Tool Calling 与结构化输出

## 学习目标

理解工具 schema 如何进入模型上下文、模型如何请求调用、宿主如何回送结果，并区分 Tool Calling 与结构化最终输出。

## 1. Tool Calling 的本质

Tool Calling 不是模型真的执行了函数。模型只是生成一个带有工具名、调用编号和参数的结构化意图。宿主收到意图后才决定验证、审批、执行或拒绝。执行结果也不会自动进入模型，必须作为与调用编号对应的 Tool Result 放回下一次请求。

调用编号承担关联作用。并发工具调用、重试和流式参数都依赖它把请求与结果配对。若宿主丢失调用编号，模型无法可靠判断哪个结果属于哪个动作。

## 2. Schema 的三种作用

工具 schema 同时承担：帮助模型选择工具；约束参数形状；帮助宿主验证输入。名称和描述影响模型的语义选择，JSON Schema 影响参数生成和确定性验证。Schema 合法并不等于业务合法，例如 `amount: 1000000` 类型正确但可能超过用户权限。

工具描述应写清“做什么、何时用、何时不用、关键参数和返回语义”。重叠工具会增加选择歧义；庞大工具目录会占用上下文并降低发现质量。

## 3. 两类结构化输出

函数调用用于连接模型与应用能力；结构化最终输出用于让最终答案符合业务 schema。前者通常触发外部动作，后者只是约束回复形状。一个 Agent 可以先调用多个工具，再以结构化对象结束。

## 4. 完整生命周期

1. Host 提供指令、消息和工具 schema；
2. Model 返回普通答案或一个/多个 Tool Call；
3. Host 解析并验证名称、参数和调用编号；
4. Policy 判断拒绝、审批或执行；
5. Tool 返回结构化结果或规范化错误；
6. Host 将结果关联到原调用；
7. Model 继续推理，或输出最终答案。

## 5. 失效模式

常见问题包括不存在的工具、缺少必填参数、错误类型、注入额外字段、重复调用、结果过大、工具执行成功但结果回送失败，以及模型在工具失败后反复重试。解决方式来自宿主：严格验证、幂等键、预算、错误分类和结果裁剪。

## 6. 从内部 Schema 到真实 DeepSeek API

课程内部用扁平结构表达函数工具：`type/name/description/parameters`。DeepSeek 的
OpenAI 兼容接口要求把后三项放进 `function` 对象。这个转换属于 Model Adapter，
不应散落在 Loop 或业务工具中。

当前课程基线使用 `https://api.deepseek.com` 与 `deepseek-v4-flash` /
`deepseek-v4-pro`。旧教程常见的 `deepseek-chat`、`deepseek-reasoner` 已退出当前
基线，不能直接复制。真实实验还要区分：

- `tool_choice=auto` 允许模型自行决定；
- `tool_choice=required` 强制至少一次工具调用；
- 模型生成合法 JSON 不等于业务参数安全；
- thinking + tools 的后续请求必须回传 `reasoning_content`；
- JSON Output 保证 JSON 语法，不替代业务 Schema 校验。

`DeepSeekChatAdapter` 将提供商 Tool Call 归一化为 `ToolCall(id, name,
arguments)`。宿主随后仍要执行名称查找、参数验证、审批、幂等和错误归一化。

## 实验

使用 `ToolSpec` 和 `ToolRegistry` 实现 `add_numbers`、`add_task`、`list_tasks`。分别构造缺失字段、额外字段、错误类型和重复调用编号，观察验证与缓存行为。

完成离线实验后运行[实验 01B](../labs/01b-deepseek-api.md)，用同一工具比较 Fake
Client 与真实 DeepSeek API 的请求、响应和失败差异。

## 验收标准

- 模型永远不直接调用 Python handler；
- 未知字段在 `additionalProperties: false` 时被拒绝；
- 同一 call id 不产生两次副作用；
- 错误以模型可理解但不泄漏内部信息的结构返回。
