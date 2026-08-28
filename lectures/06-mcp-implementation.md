# 第 6 讲：MCP Server 与 Client

## 学习目标

实现可被 Inspector 验证的 MCP Server，构建 Client，并把 REST、Qt 或 CLI 自研应用适配为受控能力。

## 1. Server 设计

先定义能力边界，再选择 SDK。任务示例可以把 `list_tasks` 和 `add_task` 暴露为工具，把 `task://all` 暴露为资源，把“生成今日计划”暴露为 Prompt。每个能力都应有稳定名称、schema 和错误语义。

stdio Server 的 stdout 属于协议，普通 `print` 会破坏帧。日志应写 stderr。Server 必须处理取消、断连和重复请求，并确保资源 URI 不允许路径穿越。

## 2. Client 设计

Client 管理连接生命周期、版本协商、能力缓存、工具过滤和调用超时。不要把 Server 的全部工具无条件暴露给模型；先根据用户、会话和任务策略得到有效目录。

远程 HTTP 连接还需要考虑授权服务器发现、Token audience、短期 Token、重定向和凭据存储。Token passthrough 会破坏受众绑定，不应把上游 Token 原样转发给任意下游。

## 3. Inspector 的作用

Inspector 用于区分“Server 协议问题”和“Agent 选择问题”。先独立验证连接、能力列表、schema 和调用结果，再接入模型。如果 Inspector 都无法稳定调用，增加 Prompt 不会修复协议错误。

## 4. 适配到 Agent Loop

MCP 工具最终应归一化到本地 Tool Registry，保留来源 Server、原始名称、风险和超时。命名空间可以减少不同 Server 的同名冲突。工具结果仍进入相同的审批、Trace 和上下文裁剪流程。

## 5. MCP 作为应用 Adapter

调用自研软件时建议保留三层：Host 负责用户交互与审批，MCP Adapter 负责能力发现、协议和错误归一化，应用本体负责身份、业务规则、事务与最终副作用。这样同一应用仍可服务 GUI、普通 API 客户端和 Agent，而无需把模型逻辑写进业务代码。

REST 应用适合跨进程或跨语言集成；Qt 应用可提供只监听 loopback 的控制 API，再通过 Signal 将变化安全地送回 GUI 主线程；已有 CLI 可以使用参数数组与 JSON stdin/stdout 适配。三种方式都应避免万能命令、任意 URL 代理和任意路径访问。

Adapter 的 Token、端点和工作目录属于控制面，不能出现在 Tool schema 中。应用端必须重复校验，不能因为请求来自 MCP 就信任参数。

## 6. 失效模式

包括 Server 进程启动失败、stdout 污染、schema 热更新、工具名冲突、HTTP 断连、OAuth 过期、超时后实际写入成功，以及关闭时遗留子进程。实验需要覆盖清理和重连，而不只覆盖 happy path。

## 实验

先完成 `examples/mcp/task_server.py`，用 Client 验证 Tool 与 Resource；再完成 `labs/02b-mcp-app-integration.md` 的 REST、Qt、CLI 三条调用链。最后注入错误令牌、应用离线、外部 URL、目录穿越和 stdout 污染，按责任层归因。
