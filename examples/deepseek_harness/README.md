# DeepSeek Harness 适配说明

`lifecycle_demo.ts` 是无依赖的教学类比，只用于先证明三个不变量：Service 不重复、Event 可追踪、Effect 可清理。它不是对快速变化 API 的伪装封装。

实际实验时：

1. 在 `baseline-lock.md` 固定 deepseek-harness commit；
2. 阅读该提交的 `SAFETY.md`、Architecture、Cordis Primer/Tutorial 与 Extension Cookbook；
3. 将 Demo 的 `provide/on/dispose` 分别映射到该提交的官方 API；
4. 添加 greet Tool 与权限 Hook；
5. 用安装→调用→卸载→再次安装测试资源清理；
6. 在报告中保留“教学类比”和“官方 API”的差异表。

在项目处于开发者预览或未完成安全审计时，不连接生产凭据、账号、目录与数据。
