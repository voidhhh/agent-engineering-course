# 实验 06：完成 Mini Harness

## 目标

组合可替换模型、工具、策略、状态和事件，建立期中项目基线。

## 起点

`src/agent_course/` 已提供最小实现。先执行：

```bash
pytest
agent-course-demo
```

## 必做扩展

1. SQLite Session Store，含 revision；
2. 总步骤、总调用数、单工具超时和输出大小预算；
3. `cancelled` 状态与取消事件；
4. 运行级幂等调用缓存，不能跨 Session 误复用；
5. 可导出 JSONL Trace；
6. 第二个 Model Adapter，核心 Loop 不改动。

## 验收演示

连续演示：只读完成；写工具暂停；拒绝后继续；批准后恢复；进程重启恢复；工具超时；最大预算停止。每个结果均能在 Trace 中找到因果链。
