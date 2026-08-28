# 第 14 讲：OpenClaw 架构解构

## 学习目标

理解长驻 Gateway、Client/Node、Session、Workspace 和 Agent Runtime 如何组合为跨渠道 Agent 系统。

## 1. Gateway 是控制中心

OpenClaw 的核心不是单次 CLI 调用，而是长驻 Gateway：它接入客户端或节点、管理会话和运行，并把外部渠道与 Agent Runtime 隔开。WebSocket 连接是传输机制；身份、权限与会话路由仍需独立分析。

## 2. 典型数据流

外部消息进入 Gateway，经过身份与 Session 路由，加载 Workspace 指令、Skill 与 Memory，交给 Runtime 驱动模型和工具，再将事件或结果返回对应渠道。同一 Session 的执行通常需要串行化，避免两个运行同时改写上下文与工作区。

## 3. Workspace 是能力与风险的交汇点

工作区可能同时包含指令、Skill、Memory、文件和执行产物。它使 Agent 能长期工作，也扩大了提示注入、敏感文件暴露和持久化污染的后果。实验必须使用专用目录，并检查默认挂载、命令权限和外部发送能力。

## 4. 与普通聊天机器人的差异

长驻进程意味着连接生命周期、重连、队列、Session 锁、后台任务和升级迁移成为一等问题。多渠道意味着同一个人、账号和会话并不天然等价。Agent 的“在线”状态也不能仅由 Gateway 进程存活判断。

## 5. 实验

按官方文档固定 OpenClaw 版本，在无生产渠道、无真实凭据的环境启动本地 Gateway。接入一个测试 Client，执行只读任务；随后制造断线重连、同 Session 并发输入和工具超时，收集 Gateway 日志与运行轨迹。

### 验收标准

- 画出 Gateway、Client/Node、Runtime、Session Store 与 Workspace 边界；
- 证明同 Session 并发的实际处理方式；
- 列出进程重启后哪些状态保留、哪些丢失；
- 清理测试凭据、会话与工作区后可回到基线。
