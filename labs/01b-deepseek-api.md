# 实验 01B：真实 DeepSeek API 与 Mini Harness

## 目标

在不破坏离线可复现性的前提下，完成真实大模型 API 的对话、流式、JSON Output
和 Tool Calling，并把提供商响应适配为课程统一的 `ModelTurn`。

## 原理问题

实验前应能回答：

1. API 返回 Tool Call 后，谁真正执行函数？
2. 为什么 DeepSeek Tool Schema 与课程内部 Schema 形状不同？
3. thinking + tools 时，为什么下一次请求必须回传 `reasoning_content`？
4. 为什么真实模型测试不能替代 `ScriptedModel` 和 Fake Client 测试？
5. 哪些错误可以有限重试，哪些必须立即失败？

## 准备

```bash
python -m pip install -e ".[dev,deepseek]"
cp .env.example .env
# 在本机编辑 .env，替换 API Key 占位符
set -a
source .env
set +a
```

先设置平台余额或额度上限。不要使用真实业务数据，不要在课堂投影、终端历史、
Trace、截图或提交记录中显示 Key。

## Milestone 1：离线理解 Adapter

```bash
pytest tests/test_deepseek_adapter.py
```

阅读 `src/agent_course/deepseek.py`，逐项标注：

- 内部 Tool Schema 到 DeepSeek Function Tool 的转换；
- 规范化 assistant/tool message 到提供商消息的转换；
- Tool Call 参数 JSON 解析与错误边界；
- `reasoning_content` 与 `ModelTurn.reasoning` 的双向映射；
- `tool_choice=required` 只用于首轮、工具返回后恢复 `auto` 的原因。

## Milestone 2：四类真实调用

```bash
python -m examples.deepseek_api.demo chat "用三句话解释 Agent Loop"
python -m examples.deepseek_api.demo stream "解释 MCP 的三类参与者"
python -m examples.deepseek_api.demo json "完成 Tool Calling 实验并补充测试"
DEEPSEEK_MODEL=deepseek-v4-pro \
  python -m examples.deepseek_api.demo harness \
  "必须使用 add_numbers 工具计算 17 + 25，然后给出结果"
```

保存每次调用的模型名、thinking 配置、完成状态、Token 用量和脱敏 Trace。不得保存
API Key 或完整敏感 Prompt。

## Milestone 3：显式 Live Test

```bash
DEEPSEEK_LIVE_TEST=1 pytest -m live tests/test_deepseek_live.py
```

Live Test 默认跳过且可能产生费用。CI 不配置真实 Key；若需要定期线上验证，应使用
受保护的 CI Secret、专用低额度 Key 和单独的手动工作流，而不是普通 Push 自动执行。

## 故障注入

依次验证：

1. Key 保持占位符，确认在网络请求前失败；
2. 将模型名改成旧名称，确认课程 Adapter 拒绝过期基线；
3. Fake Client 返回非法 Tool Arguments JSON，确认不会执行工具；
4. 删除 thinking 工具轮次中的 reasoning 映射，记录后续 400；
5. 模拟 401、402、422、429、500、503，设计错误分类和有上限退避；
6. 让 `max_tokens` 太小导致 JSON 截断，确认解析失败被显式报告。

## 验收

- `.env.example` 只有占位符，`.env` 不进入 Git；
- 离线测试无 Key、无网络、无费用即可通过；
- Live Test 必须双重显式启用；
- API 响应先经 Adapter 归一化，Loop 不依赖 SDK 对象；
- 工具参数在执行前仍经过宿主验证；
- Trace 能区分模型调用、工具调用、工具结果与最终答案；
- 报告注明模型、接口、日期、Token 和成本，且不泄漏凭据。

## 官方资料

- [DeepSeek First API Call](https://api-docs.deepseek.com/)
- [Chat Completions](https://api-docs.deepseek.com/api/create-chat-completion/)
- [Responses API](https://api-docs.deepseek.com/guides/responses_api/)
- [Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/)
- [Tool Calls](https://api-docs.deepseek.com/guides/tool_calls/)
- [JSON Output](https://api-docs.deepseek.com/guides/json_mode/)
- [Error Codes](https://api-docs.deepseek.com/quick_start/error_codes/)
