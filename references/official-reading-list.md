# 官方资料阅读顺序

最后核对：2026-08-28。优先使用固定版本页面、官方文档、官方仓库和论文。

## 1. Agent 与 Tool Calling

1. [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
2. [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
3. [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
4. [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
5. [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

## 2. MCP

1. [MCP Introduction](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)
2. [Architecture](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)
3. [Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
4. [Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
5. [Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
6. [Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)
7. [Build a Server](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server)
8. [Build a Client](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-client)
9. [Inspector](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector)
10. [Authorization Security](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations)
11. [MCP Python SDK v2: What's New](https://py.sdk.modelcontextprotocol.io/v2/whats-new/)
12. [MCP Python SDK Repository](https://github.com/modelcontextprotocol/python-sdk)

## 3. Agent Skills

1. [Overview](https://agentskills.io/home)
2. [Specification](https://agentskills.io/specification)
3. [Best Practices](https://agentskills.io/skill-creation/best-practices)
4. [Evaluating Skills](https://agentskills.io/skill-creation/evaluating-skills)
5. [OpenAI Build Skills](https://learn.chatgpt.com/docs/build-skills)

## 4. Framework 与 Harness

1. [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents)
2. [Quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart)
3. [Running Agents](https://developers.openai.com/api/docs/guides/agents/running-agents)
4. [Orchestration and Handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration)
5. [Guardrails and Human Review](https://developers.openai.com/api/docs/guides/agents/guardrails)
6. [Integrations and Observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability)
7. [Codex as an Open Agent Harness](https://developers.openai.com/blog/codex-as-a-platform)
8. [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## 4.1 DeepSeek API

1. [Your First API Call](https://api-docs.deepseek.com/)
2. [Models and Pricing](https://api-docs.deepseek.com/quick_start/pricing/)
3. [Chat Completions API](https://api-docs.deepseek.com/api/create-chat-completion/)
4. [Responses API](https://api-docs.deepseek.com/guides/responses_api/)
5. [Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/)
6. [Tool Calls](https://api-docs.deepseek.com/guides/tool_calls/)
7. [JSON Output](https://api-docs.deepseek.com/guides/json_mode/)
8. [Error Codes](https://api-docs.deepseek.com/quick_start/error_codes/)
9. [Rate Limit and Isolation](https://api-docs.deepseek.com/quick_start/rate_limit/)
10. [Change Log](https://api-docs.deepseek.com/updates/)

阅读时以当前模型名和变更记录为准。旧博客中的 `deepseek-chat`、
`deepseek-reasoner` 不作为 2026-08 课程配置依据。

## 5. Hermes

1. [Hermes 4 Technical Report](https://arxiv.org/abs/2508.18255)
2. [Hermes 4 14B Model Card](https://huggingface.co/NousResearch/Hermes-4-14B/blob/main/README.md)
3. [Hermes Agent Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)
4. [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)
5. [Agent Loop](https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop)
6. [Tools Runtime](https://hermes-agent.nousresearch.com/docs/developer-guide/tools-runtime)
7. [Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
8. [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
9. [MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
10. [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security)

## 6. OpenClaw

1. [Getting Started](https://docs.openclaw.ai/start/getting-started)
2. [Gateway Architecture](https://docs.openclaw.ai/concepts/architecture)
3. [Agent Loop](https://docs.openclaw.ai/concepts/agent-loop)
4. [Context](https://docs.openclaw.ai/concepts/context)
5. [Memory Architecture](https://docs.openclaw.ai/concepts/memory-architecture)
6. [Skills](https://docs.openclaw.ai/tools/skills)
7. [MCP](https://docs.openclaw.ai/tools/mcp)
8. [Security](https://docs.openclaw.ai/gateway/security)

## 7. DeepSeek Harness

1. [Repository](https://github.com/deepseek-ai/deepseek-harness)
2. [Safety](https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md)
3. [Architecture](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)
4. [Cordis Primer](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-primer.md)
5. [Cordis Tutorial](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-tutorial/index.md)
6. [Into the Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-tutorial/07-into-the-harness.md)
7. [Extension Cookbook](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cookbook/extension-cookbook.md)

## 8. Eval

1. [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
2. [Agent Improvement Loop](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop)
3. [Testing Agent Skills with Evals](https://developers.openai.com/blog/eval-skills)
