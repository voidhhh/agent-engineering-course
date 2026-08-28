# 实例 C：MCP 调用自研 CLI 报告软件

数据流：`MCP Host → stdio MCP Adapter → 参数数组 + JSON stdin → Report CLI → 受限工作目录`。这个实例用于说明并非所有旧应用都要先改造成 HTTP 服务；稳定 CLI 也可以成为 Adapter 边界。

## 配置

```bash
export COURSE_REPORT_DIR=/tmp/agent-course-reports
python -m examples.app_integration.cli_reports.mcp_server
```

MCP 工具可以生成、列出和读取 Markdown 报告。Adapter 使用参数数组而非 shell 字符串，设置超时，并只接受简单 `.md` 文件名；应用拒绝目录穿越、过大请求、无效数值和覆盖已有文件。

## 直接测试应用

```bash
printf '%s' '{"operation":"generate","title":"Demo","filename":"demo.md","rows":[{"label":"passed","value":10}]}' \
  | python -m examples.app_integration.cli_reports.report_app --workspace /tmp/agent-course-reports
```

## 故障实验

传入 `../escape.md`、让应用超时、返回非 JSON、重复生成同名文件。检查 MCP Adapter 是否把进程错误归一化为工具错误，且不会退回到 shell 拼接执行。
