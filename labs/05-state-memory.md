# 实验 05：State、Session 与 Memory

## 目标

实现持久会话、并发保护和可审计 Memory，不把消息重放误称为长期记忆。

## 任务

1. 设计 SQLite 表：`sessions`、`messages`、`checkpoints`、`memories`；
2. Session 使用 `revision` 乐观锁；
3. Memory 包含内容、来源、创建时间、有效期、敏感级别和删除状态；
4. 对 12 轮对话实现全量、滑动窗口、摘要加最近消息三种构建策略；
5. 在审批暂停后重启进程，再从原 Checkpoint 恢复。

## 故障注入

同时更新同一 Session；在摘要前放入未完成工具调用；召回一条与当前事实冲突的旧 Memory；删除 Memory 后确认索引与原文都不可再召回。

## 验收

无静默覆盖、无跨会话串话；摘要保留关键不变量；恢复不重复执行副作用；Memory 的写入和删除均有审计事件。
