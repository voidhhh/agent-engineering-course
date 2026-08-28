# Hermes 实验记录模板

本目录不复制 Hermes Agent 或模型权重。按官方 Quickstart 在隔离环境安装固定版本，并将证据填入自己的实验分支。

## 版本锁

- Hermes 模型标识/修订：
- 推理服务与版本：
- Chat template：
- Hermes Agent tag/commit：
- 安装日期：
- 配置摘要（无密钥）：

## 模型实验

记录每个 Case 的原始消息、工具 schema、模型原始输出、解析结果、工具调用和最终分类：正确 / 选错工具 / 参数错 / 格式错 / 答案错。

## Agent 实验

记录 Prompt 组装、Loop 步骤、Tool、Skill、Memory、MCP 与工作区变更。对“学习”结论必须附文件或状态变化证据，并明确它不是模型权重训练。

## 清理

删除实验工作区、测试 Memory/Skill、模型服务缓存（若需）和测试凭据；确认没有后台进程与真实账号连接。
