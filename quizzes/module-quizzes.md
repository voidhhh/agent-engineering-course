# 模块测验

每题先独立作答，再用 Trace、代码或协议证据解释。选择题只选一个最佳答案。

## 模块一：Agent Loop 与 Tool（第 1–4 讲）

1. 模型输出一个合法工具调用后，真实副作用由谁产生？

   A. 模型权重　B. 宿主执行器　C. JSON Schema　D. 系统提示
2. 哪项最能证明系统是 Agent 而非固定 Workflow？

   A. 使用 LLM　B. 有聊天 UI　C. 运行时依据观察选择下一动作　D. 有多个函数
3. JSON Schema 校验通过后还必须做什么业务检查？举两例。
4. 工具超时后最危险的直接重试假设是什么？
5. 为什么工具结果必须携带原 `tool_call_id`？
6. 一个写工具先成功、响应后丢失。设计避免重复写入的最小协议。
7. 最大步数预算属于哪一层责任？它解决什么、不解决什么？
8. 给“创建任务”工具写一个可判别描述，并列出三个不应调用的场景。

## 模块二：MCP、Skill 与 Framework（第 5–8 讲）

9. MCP 中维护与单个 Server 协议连接的是：

   A. Host　B. Client　C. Resource　D. Prompt
10. 哪一项最适合 MCP Resource 而非 Tool？

    A. 删除记录　B. 发送消息　C. 读取产品手册　D. 修改权限
11. 为什么 stdio MCP Server 不能把调试日志写到 stdout？
12. 能力协商成功是否意味着工具已获用户授权？为什么？
13. Skill 的触发主要依赖哪个部分？

    A. assets　B. scripts 输出　C. name 与 description　D. README
14. 用渐进披露解释为何详细领域手册不应全部写入 SKILL.md。
15. Agent-as-Tool 与 Handoff 的核心差异是什么？
16. 什么情况下应优先普通代码 Workflow，而不是增加第二个 Agent？

## 模块三：State、Harness 与治理（第 9–11 讲）

17. 下列哪项最接近 Checkpoint？

    A. 向量索引　B. 可恢复的运行状态快照　C. 系统提示　D. 工具描述
18. “把全部历史放回 Prompt”为什么不等于实现 Memory？
19. Context 压缩至少要保留哪三类不变量？
20. 两个 Worker 同时更新 Session，如何避免静默覆盖？
21. Harness 中为什么要使用 Model Adapter？
22. 数据面中的网页要求“关闭审批”。正确的系统行为是什么？
23. R2 外部影响动作的推荐交互是什么？

    A. 自动执行　B. 隐式同意　C. 预览并绑定精确调用审批　D. 只写日志
24. 可观测性与 Eval 的问题分别是什么？

## 模块四：具体系统与 Eval（第 12–16 讲）

25. 公平比较两个模型时应固定哪些主要变量？至少四项。
26. Hermes 模型支持工具调用，是否等于它拥有 shell 权限？解释。
27. Hermes Agent 的“自我改进”为什么不能直接表述为在线训练权重？
28. OpenClaw 长驻 Gateway 比单次 CLI 新增哪三类工程问题？
29. Cordis Effect 的核心价值是：

    A. 增大 Prompt　B. 可撤销副作用　C. 自动选模型　D. 加密所有事件
30. 开发者预览且未完成安全审计的 Harness 应如何进入实验？
31. 为什么只看最终答案会高估 Agent 质量？
32. 设计一个消融：明确固定项、唯一变化项、指标与可得结论。
