# 实例 A：MCP 调用自研 REST 任务软件

数据流：`MCP Host → stdio MCP Adapter → localhost REST API → TaskStore`。应用本体完全不知道模型存在；MCP Adapter 只做协议与错误归一化，业务校验仍由 REST 应用执行。

## 启动

在终端 1：

```bash
export COURSE_APP_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(24))')"
python -m examples.app_integration.rest_tasks.app
```

在同样设置 `COURSE_APP_TOKEN` 的终端 2，将 MCP Server 命令配置为：

```bash
python -m examples.app_integration.rest_tasks.mcp_server
```

可用工具：健康检查、创建任务、列出任务、完成任务。写工具应在 Host 中配置审批。

## 观察点

关闭 REST 应用、使用错误令牌、传空标题、重复完成和修改 `COURSE_TASK_API` 指向非 loopback 地址。Adapter 应返回明确错误，且 SSRF 目标被本地 URL 校验拒绝。
