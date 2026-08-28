# 实验手册

实验围绕同一个“本地知识与任务助理”，默认只读写仓库内测试数据。离线实验无需模型 Key；平台实验必须使用隔离目录、测试账号和最小权限。

| 实验 | 对应讲次 | 核心交付 |
|---|---:|---|
| [01 Tool 与 Loop](01-tool-loop.md) | 2–4 | 可测工具契约与最小循环 |
| [01B DeepSeek 真实 API](01b-deepseek-api.md) | 2–3 | Chat/Stream/JSON/Tool Calling + Adapter |
| [02 MCP Server/Client](02-mcp.md) | 5–6 | stdio 服务、资源与调用证据 |
| [02B MCP 调用自研应用](02b-mcp-app-integration.md) | 6 | REST、Qt、CLI 三类 Adapter |
| [03 Agent Skill](03-skill.md) | 7 | `research-brief` 与触发 Eval |
| [04 Agent Framework](04-agent-framework.md) | 8 | SDK 版本与编排对照 |
| [05 State 与 Memory](05-state-memory.md) | 9 | SQLite Session 与压缩实验 |
| [06 Mini Harness](06-mini-harness.md) | 10 | Adapter/Loop/Policy/Store/Event |
| [07 故障与治理](07-failure-governance.md) | 11 | 故障注入矩阵 |
| [08 Hermes](08-hermes.md) | 12–13 | 模型/运行时分离报告 |
| [09 OpenClaw](09-openclaw.md) | 14 | Gateway 生命周期报告 |
| [10 DeepSeek Harness](10-deepseek-harness.md) | 15 | Plugin/Hook 生命周期实验 |
| [11 Eval 与期末](11-evals.md) | 16 | 评测结果与消融报告 |

## 通用证据包

每个实验提交：`README` 结论、版本锁、配置、可运行命令、测试结果、原始 Trace、失败样本和清理记录。截图只能辅助说明，不能替代机器可读日志。

## 通用安全规则

1. 不连接生产渠道，不使用个人主目录和真实业务数据；
2. 不把 Key 写进代码、配置样例、Trace 或提交历史；
3. 外部发送、删除、安装和 shell 操作必须显式审批；
4. 实验结束移除容器、测试凭据、后台进程和持久数据；
5. 快速变化的项目以固定 tag/commit 重现，不使用无版本的“latest”作结论。
6. Live API 测试默认跳过，必须通过环境变量显式启用并设置费用上限。
