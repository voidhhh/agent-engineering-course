# 实验 01：Tool 与最小 Agent Loop

## 目标

验证 Tool Calling 的完整闭环，并能把模型问题与 Loop 问题分开定位。

## 准备

```bash
python -m pip install -e ".[dev]"
pytest tests/test_tools.py tests/test_loop.py
agent-course-demo
```

## 任务

1. 阅读 `ToolSpec`、`ToolRegistry`、`ScriptedModel` 和 `AgentLoop`；
2. 画出一次 `add_numbers` 调用中消息与调用 ID 的变化；
3. 新增 `complete_task` 工具，限制 `task_id` 为整数；
4. 写测试覆盖正常完成、缺参、未知字段、未知工具、重复调用 ID 和最大步数；
5. 把工具异常作为 tool message 回送，而不是让进程崩溃。

## 故障注入

让模型连续 9 次请求工具、返回不存在的工具，以及对相同调用 ID 提供不同参数。记录当前实现的行为，并讨论调用缓存应按何种作用域隔离。

## 验收

- 所有路径离线可测；
- 调用结果精确绑定原 ID；
- 重放调用不重复写入；
- 步数预算耗尽产生明确失败原因。
