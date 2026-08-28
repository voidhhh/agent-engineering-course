# MCP 调用自研应用：三种 Adapter

| 实例 | 应用接口 | MCP 提供的价值 | 主要边界 |
|---|---|---|---|
| [REST Tasks](rest_tasks/README.md) | localhost REST | Tool schema、发现、统一错误 | 令牌、SSRF、业务校验 |
| [Qt Notes](qt_notes/README.md) | Qt 内嵌 loopback API | 语义化桌面控制 | GUI 主线程、用户可见副作用 |
| [CLI Reports](cli_reports/README.md) | JSON stdin/stdout 子进程 | 旧应用适配、超时、输出归一化 | 命令注入、路径、进程生命周期 |

## 共同设计

应用接口是领域边界，MCP Server 是协议 Adapter，Host 是审批与用户交互边界。三者不要合并成“让模型直接执行任意命令”。

共同不变量：

- 只暴露明确的语义动作，不提供万能 `execute`；
- 应用端重复校验身份、参数与资源范围；
- MCP 错误不伪装为成功文本；
- 写工具由 Host 按风险分级审批；
- Adapter 设置超时、输出上限和结构化 Trace；
- 令牌来自环境或密钥系统，不进入 Tool schema、Prompt 或仓库。

运行 `python -m examples.app_integration.smoke` 可在不启动 Qt GUI 的情况下，通过 MCP v2 内存传输依次调用三种应用 Adapter。
