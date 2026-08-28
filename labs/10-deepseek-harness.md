# 实验 10：DeepSeek Harness Plugin 与 Hook

## 目标

用最小插件验证 Cordis 的 Service、Event、Effect 与卸载语义。

## 环境约束

项目若仍处开发者预览或未完成安全审计，只能在隔离环境研究。固定仓库 commit；不接生产 API、账号、目录或数据。

## 任务

1. 先完成官方 Cordis Primer/Tutorial；
2. 按当前固定提交改写 `examples/deepseek_harness/` 的概念骨架；
3. 实现一个 greet Tool Plugin；
4. 实现权限 Hook：只读自动允许，外部影响请求暂停审批；
5. 记录安装、调用、卸载、再次安装的 Service 和监听器数量；
6. 制造依赖缺失与初始化异常，验证部分注册能清理。

## 验收

Effect 清理后状态回到基线；权限决定含理由和策略版本；报告引用固定 commit，并明确哪些代码来自官方 API、哪些是教学适配。
