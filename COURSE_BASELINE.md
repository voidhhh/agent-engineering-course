# 课程技术基线

最后核对日期：2026-08-28。

## 固定基线

- MCP：以 `2026-07-28` 规范与 Python SDK `2.x` 稳定线为课程协议/示例基线。
- Agent Skills：以 `agentskills.io/specification` 的公开规范为格式基线。
- Python：建议 3.11 或更高版本；核心 Mini Harness 只依赖标准库。
- 测试：pytest；所有默认测试必须离线、确定性运行。
- DeepSeek API：Base URL 为 `https://api.deepseek.com`；课程模型名固定为
  `deepseek-v4-flash`、`deepseek-v4-pro`，并以 OpenAI 兼容 Chat Completions /
  Responses API 为接口基线。

DeepSeek 官方变更记录显示，旧名称 `deepseek-chat`、`deepseek-reasoner` 已在
2026-07-24 后停止作为当前模型入口使用。课程案例不得沿用旧教程的模型名。V4
thinking 默认开启，使用 `thinking.type` 和 `reasoning_effort=low/high/max` 控制；
thinking + tools 的后续请求必须保留 `reasoning_content`。

真实 API 测试必须满足：Key 仅来自环境变量；`.env` 不入库；默认 CI 跳过 Live
Test；使用专用低额度 Key；记录模型、时间、Token 与脱敏 Trace。

## 快速演进项目

Hermes Agent、OpenClaw 与 DeepSeek Harness 更新频繁。授课前必须：

1. 在 `baseline-lock.md` 中记录使用的 release tag 或 Git commit；
2. 保存安装命令与依赖版本；
3. 用本仓库的 smoke tasks 验证基本功能；
4. 记录与讲义不一致的接口；
5. 不直接把 `main`/`master` 当作稳定教学环境。

DeepSeek Harness 官方安全说明将其标记为尚未完成安全审计的开发者预览软件。该实验应运行在一次性虚拟机、容器或专用环境中，并且只挂载实验目录。

## 比较实验的控制变量

比较不同 Harness 时尽量保持以下项目一致：

- 模型与推理配置；
- system instructions；
- Tool/MCP schema；
- Skill 内容；
- 任务输入与随机种子；
- 超时、最大步数和审批策略；
- 评分脚本。

若某个平台无法保持变量一致，必须在报告中说明，禁止把结果直接归因于 Harness。
