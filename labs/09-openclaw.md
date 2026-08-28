# 实验 09：OpenClaw Gateway

## 目标

从运行证据理解 Gateway、Session、Workspace 和 Agent Runtime 的边界。

## 环境约束

使用官方 Getting Started 和固定版本；仅启动本地 Gateway 与测试 Client；不连接 Telegram、Slack、邮件或其他真实渠道；使用临时 Workspace 与测试密钥。

## 任务

1. 记录 Gateway 启动、Client 连接和 Session 创建；
2. 完成一个只读文件任务，追踪消息到工具结果的路径；
3. 同一 Session 同时发送两条输入，观察串行化/排队；
4. 断开 Client 再重连，区分连接状态与 Session 状态；
5. 重启 Gateway，列出持久与非持久状态；
6. 执行清理并检查无后台进程、凭据和测试工作区残留。

## 验收

提交架构图、版本、启动命令、三次故障轨迹、状态表和清理证据。任何未经验证的行为必须标为假设。
