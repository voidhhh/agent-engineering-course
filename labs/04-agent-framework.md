# 实验 04：Agent Framework 对照

## 目标

将手写 Loop 映射到 OpenAI Agents SDK，并理解编排抽象的成本。

## 准备

阅读官方 Agents SDK 概览、Running Agents、Orchestration、Guardrails 和 Observability。API 实验需自行配置测试 Key；离线课程验收不要求调用付费服务。

```bash
python -m pip install -e ".[openai-agents]"
python examples/openai_agents/assistant.py
```

## 三组实现

1. 一个 Agent 直接使用任务工具；
2. 主 Agent 把摘要专家作为 Tool 调用，主 Agent 保留最终答复；
3. 路由 Agent Handoff 给执行专家，由专家接管分支。

## 记录

比较模型调用数、工具调用数、状态传递、审批暂停、Trace 可读性和错误恢复代码量。不要仅比较最终文案。

## 验收

能指出 SDK Runner 中与第 3 讲 Loop 对应的步骤；能解释 Agent-as-Tool 与 Handoff 的控制权差异；能从暂停状态恢复原运行而非新开一轮。
