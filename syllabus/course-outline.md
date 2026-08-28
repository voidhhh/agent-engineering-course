# 课程大纲

## 一、课程定位

本课程训练学习者从协议、运行循环和工程边界理解 Agent 系统。课程不把“能安装某个产品”作为掌握标准，而要求学习者能够解释、重建、观测、评测和约束 Agent。

## 二、学习成果

完成课程后，学习者应能够：

1. 准确区分 Model、Agent、Workflow、Tool、MCP、Skill、Framework 与 Harness；
2. 独立实现具备 Tool Calling、终止预算和错误归一化的 Agent Loop；
3. 用 Adapter 将真实 DeepSeek API 接入统一 Loop，并分离离线测试与付费 Live Test；
4. 构建并调试 stdio 与 Streamable HTTP MCP Server/Client；
5. 编写、触发、评测和维护符合 Agent Skills 规范的 Skill；
6. 设计 Context、Session、Memory、Checkpoint 与 Event Trace；
7. 实现审批策略、幂等调用、超时恢复、并发隔离和最小权限控制；
8. 从源码和运行轨迹分析 Hermes Agent、OpenClaw 与 DeepSeek Harness；
9. 用控制变量和统一任务集比较模型与 Harness，而不是凭主观体验下结论。

## 三、讲次安排

| 讲次 | 主题 | 原理解构 | 实验交付 |
|---:|---|---|---|
| 1 | Agent 系统全景 | 分层、责任边界、数据流 | 系统分层图 |
| 2 | Tool Calling | JSON Schema、Provider 映射、参数、结果回送 | 函数工具 + DeepSeek API |
| 3 | 最小 Agent Loop | 推理—行动—观察、Adapter、停止条件 | 离线循环 + Live 对照 |
| 4 | 工具工程 | 描述、验证、错误、幂等、超时 | 工具契约测试 |
| 5 | MCP 架构 | Host/Client/Server、JSON-RPC、能力协商 | 协议时序分析 |
| 6 | MCP 实现 | 原语、传输、应用 Adapter、权限边界 | REST/Qt/CLI MCP 集成 |
| 7 | Agent Skills | 触发、渐进披露、资源组织、Eval | `research-brief` Skill |
| 8 | Agent Framework | Runner、Handoff、Guardrail、Trace | SDK 重构版 Agent |
| 9 | Context/Session/Memory | 可见上下文、持久状态、召回与压缩 | SQLite 会话实验 |
| 10 | Harness 核心 | Adapter、Registry、Loop、Event、Store | Mini Harness |
| 11 | 可靠性与治理 | 审批、沙箱、并发、恢复、审计 | 故障注入矩阵 |
| 12 | Hermes 模型 | 混合推理、工具调用格式、模型评测 | 同任务模型对比 |
| 13 | Hermes Agent | Loop、Tool、Memory、Skill、MCP | 轨迹与学习闭环分析 |
| 14 | OpenClaw | Gateway、Session、Workspace、Runtime | 本地 Gateway 实验 |
| 15 | DeepSeek Harness | Cordis、Plugin、Service、Event、Effect | Tool Plugin + Hook |
| 16 | Agent Eval | 任务、轨迹、安全、恢复、消融 | 期末评测与答辩 |

## 四、学时建议

每讲 4 学时：

- 30 分钟：问题情境与前测；
- 60 分钟：机制和数据流解构；
- 30 分钟：源码/协议证据阅读；
- 90 分钟：实验；
- 30 分钟：失败注入与讨论；
- 30 分钟：验收、反思和课后任务。

## 五、连续实验主线

整个课程只维护一个“本地知识与任务助理”：

1. 第 2 讲把领域能力实现为 Python 函数，并用 DeepSeek API 返回真实 Tool Call；
2. 第 3～4 讲用同一 Loop 对照 ScriptedModel、Fake Client 和真实模型；
3. 第 5～6 讲将能力迁移到 MCP；
4. 第 7 讲将研究流程写成 Skill；
5. 第 8～11 讲加入框架、状态和 Harness；
6. 第 12～15 讲接入具体模型和运行实现；
7. 第 16 讲用同一任务集完成对照实验。

## 六、不在核心范围内的内容

模型预训练、全参数微调、大规模向量数据库运维、复杂前端开发和公有云厂商部署不是本课程核心。它们可以作为后续专题，但不应挤占 Agent Loop、协议、安全和 Eval 的训练时间。
