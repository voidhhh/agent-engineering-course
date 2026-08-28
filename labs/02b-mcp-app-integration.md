# 实验 02B：让 MCP 调用自研应用软件

## 目标

把 MCP Server 设计成应用 Adapter，而不是把业务逻辑、任意 shell 和模型权限混在一个进程中。完成三条真实调用链：REST、Qt 和 CLI。

## 共同架构

```text
MCP Host ──MCP── Adapter ──应用原生接口── 自研应用 ──领域状态/副作用
   │                 │                         │
审批与用户交互    协议/错误归一化          身份、业务校验、事务
```

Adapter 只暴露窄而可判别的语义工具。禁止设计 `execute_anything(command)`、任意 URL 代理或任意文件路径工具。

## A. REST 任务软件

```bash
python -m pip install -e ".[dev,mcp]"
export COURSE_APP_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(24))')"
python -m examples.app_integration.rest_tasks.app
```

在相同令牌环境下，以 `python -m examples.app_integration.rest_tasks.mcp_server` 作为 MCP stdio Server。调用健康检查、创建、列出和完成任务；抓取 REST 与 MCP 两层错误。

## B. Qt 桌面笔记软件

```bash
python -m pip install -e ".[mcp,qt]"
export COURSE_APP_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(24))')"
python -m examples.app_integration.qt_notes.qt_app
```

配置 MCP Server 为 `python -m examples.app_integration.qt_notes.mcp_server`。通过 Agent 创建笔记并让窗口聚焦指定笔记。解释为何 HTTP 工作线程不能直接修改 Qt Widget，以及 Signal 如何跨线程回到主线程。

## C. CLI 报告软件

设置 `COURSE_REPORT_DIR=/tmp/agent-course-reports`，以 `python -m examples.app_integration.cli_reports.mcp_server` 启动 Adapter。生成、列出和读取报告；确认 Adapter 使用参数数组与 JSON stdin，不拼接 shell 字符串。

## 自动 Smoke Test

```bash
python -m examples.app_integration.smoke
pytest tests/test_app_integrations.py tests/test_mcp_app_smoke.py
```

Smoke Test 通过 MCP v2 内存传输调用三个 Adapter；Qt 路径测试控制 API 与 UI Signal 回调，不要求 CI 具备桌面显示器。

## 故障注入

| 故障 | 预期 |
|---|---|
| 错误 Bearer Token | 应用返回 401，MCP 报工具错误 |
| REST 应用离线 | 有界超时，不虚构成功 |
| API 指向外部域名 | loopback 校验拒绝，防止 SSRF |
| Qt 应用关闭 | MCP 不尝试用坐标点击替代 |
| CLI 文件名 `../x.md` | 应用拒绝目录穿越 |
| CLI 返回非 JSON | Adapter 归一为协议错误 |
| 同名报告重放 | 不覆盖已有文件，要求新决策 |

## 验收

- 三条调用链均有应用本体、Adapter、测试和启动说明；
- REST/Qt 控制 API 只监听 loopback 且要求令牌；
- 应用端独立执行业务校验；
- 写工具能在 Host 层配置审批；
- 错误可区分 MCP、Adapter、应用协议和领域层；
- Trace 不含令牌、完整敏感正文或任意系统路径。
