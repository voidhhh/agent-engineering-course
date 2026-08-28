# 实验 08：Hermes 模型与 Hermes Agent

## 目标

以控制变量区分 Hermes 模型能力与 Hermes Agent Harness 能力。

## A. 模型实验

1. 在 `baseline-lock.md` 固定模型、模板、推理设置与推理服务；
2. 使用 `evals/functional.jsonl` 中适用的工具任务；
3. 固定 Harness 和工具，只替换模型；
4. 保存原始输出，统计选择、参数、格式和最终结果错误。

## B. 运行时实验

1. 固定 Hermes Agent tag/commit，在容器或专用目录安装；
2. 不挂载个人主目录，不连接真实外部账号；
3. 完成研究简报任务，记录 Loop、Tool、Skill、Memory、MCP 轨迹；
4. 比较 Skill/Memory 写入前后目录，并禁用新增内容重跑；
5. 清理持久数据，验证恢复基线。

## 验收

报告三栏分开写“官方文档/源码事实”“项目公开主张”“本次实验观察”；不得把文件级学习写成模型权重训练。
