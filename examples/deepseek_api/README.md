# DeepSeek 真实 API 案例

本目录把真实模型调用接入第 2～3 讲的 Tool Calling 和 Mini Harness。它使用
DeepSeek 官方 OpenAI 兼容接口，但所有默认测试仍然离线运行。

## 当前课程基线

- Base URL：`https://api.deepseek.com`
- 默认模型：`deepseek-v4-flash`
- Agent 对照模型：`deepseek-v4-pro`
- 旧名称 `deepseek-chat`、`deepseek-reasoner` 已停止作为课程基线使用
- API Key 仅从 `DEEPSEEK_API_KEY` 读取

版本和模型名会变化，运行前应再次核对 DeepSeek 官方文档及
[`COURSE_BASELINE.md`](../../COURSE_BASELINE.md)。

## 安装与配置

```bash
python -m pip install -e ".[dev,deepseek]"
cp .env.example .env
# 编辑 .env，只在本机填入真实 Key
set -a
source .env
set +a
```

`.env` 已被 `.gitignore` 排除。示例还会拒绝明显的占位符，避免误以为请求已经
发出。不要把 Key 写进命令历史、截图、Trace、异常报告或测试数据。

## 四个真实案例

### 1. Chat Completions

```bash
python -m examples.deepseek_api.demo chat "用三句话解释 Agent Loop"
```

展示环境变量配置、同步请求、thinking 开关、用量归一化和提供商错误边界。

### 2. Responses API 流式输出

```bash
python -m examples.deepseek_api.demo stream "解释 MCP Host、Client、Server 的关系"
```

只输出 `response.output_text.delta`，不默认记录推理文本。Responses API 使用语义
SSE 事件，并以 `response.completed`、`response.incomplete` 或
`response.failed` 结束，不应按 Chat Completions 的 `[DONE]` 规则解析。

### 3. JSON Output

```bash
python -m examples.deepseek_api.demo json "完成最小 Agent Loop，并为工具异常写测试"
```

同时设置 `response_format={"type":"json_object"}`，并在提示中明确要求 JSON 及
给出格式示例。调用后仍使用 `json.loads` 验证，不把“JSON 模式”误当成业务
Schema 验证。

### 4. DeepSeek + Mini Harness + Tool Calling

```bash
DEEPSEEK_MODEL=deepseek-v4-pro \
python -m examples.deepseek_api.demo harness \
  "必须使用 add_numbers 工具计算 17 + 25，然后给出结果"
```

该案例走完整链路：DeepSeek 返回 Tool Call，Adapter 归一化为 `ModelTurn`，
Mini Harness 验证并执行本地工具，再把 Tool Result 回送模型。首次请求设置
`tool_choice=required`，工具结果返回后自动恢复为 `auto`，使模型可以给出最终答案。

thinking 模式下，DeepSeek 要求带工具的后续请求完整回传前一轮
`reasoning_content`。课程核心以通用字段 `ModelTurn.reasoning` 保存，Adapter 再映射
回提供商字段；Trace 默认不记录其正文。

## 离线测试与付费 Live Test

```bash
# Fake client，绝不联网
pytest tests/test_deepseek_adapter.py

# 显式启用，可能产生费用
DEEPSEEK_LIVE_TEST=1 pytest -m live tests/test_deepseek_live.py
```

Live Test 默认跳过。开启前先在平台侧设置余额/额度限制，并确认没有把真实数据放入
Prompt。401、402、422 不应重试；429、500、503 只能做有上限的退避重试。
