# 实验 02：MCP Server 与 Client

## 目标

把任务能力通过 MCP 暴露，并观察生命周期、能力协商和传输边界。

## 准备

先阅读当前锁定版本的 MCP Architecture、Specification、Build a Server、Python SDK v2 What's New 和 Inspector。然后：

```bash
python -m pip install -e ".[mcp]"
python examples/mcp/task_server.py
```

stdio 模式等待 Client 输入是正常现象；不要向 stdout 打印调试日志。

## 任务

1. 用 Inspector 或 `task_client.py` 建立连接并检查协商后的协议信息；
2. 列出工具，调用 `add_task` 与 `list_tasks`；
3. 读取 `tasks://all` Resource；
4. 保存一次初始化和一次工具调用的结构化记录；
5. 将同一服务切换为 Streamable HTTP，记录认证与部署边界的变化。

## 故障注入

分别测试无效参数、未知工具、Server 中断、Client 超时和 stdout 污染。回答哪些错误属于 JSON-RPC、哪些属于 Tool result、哪些属于传输。

## 验收

能解释 Host/Client/Server 三者责任；两种传输均不暴露生产凭据；Server 端仍执行业务授权，而不是信任模型参数。
