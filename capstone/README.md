# 期末项目：跨模型与 Harness 的可复现实验

## 核心问题

选择一个明确问题，例如：“在本地知识与任务助理上，Skill 对任务成功与上下文成本有何影响？”或“固定模型时，Mini Harness 与某公开 Harness 的恢复行为有何差异？”

## 最低实验设计

- 一个 Mini Harness 基线；
- 至少两个 Hermes Agent、OpenClaw、DeepSeek Harness 相关实现或适配，总计至少三种运行实现；
- 至少两个模型配置，或一个模型上的两个 Harness 配置；
- 至少完成一次 DeepSeek 实际 API 运行，并保留同任务的离线可复现实验；
- `evals/` 36 个 Case 中至少 24 个，加 6 个自定义领域 Case；
- 每个随机配置至少重复 3 次；
- 至少两项单变量消融；
- 原始 Trace、机器评分、失败归因与完整版本锁。

实际 API 不要求运行全部 Case。应先用离线适配器完成回归，再选取代表性 Case
进行小规模在线验证，并记录模型名、接口类型、thinking 配置、输入/输出 Token、
估算费用和发生时间。报告不得包含 API Key、完整请求头或其他秘密。

## 交付结构

```text
capstone-submission/
├── README.md
├── baseline-lock.md
├── configs/
├── cases/
├── runners/
├── raw-results/
├── traces/
├── analysis/
└── report.md
```

## 答辩

10 分钟讲问题、方法和结论；8 分钟现场重现随机 Case；7 分钟从随机失败 Trace 归因。无法从汇总结果回溯到原始证据的结论不计分。

## 评分（100）

| 项目 | 分值 |
|---|---:|
| 问题与控制变量 | 15 |
| 系统实现与适配 | 20 |
| Eval/评分器质量 | 20 |
| 安全与恢复证据 | 15 |
| 分析、消融与限制 | 20 |
| 复现性与答辩 | 10 |

任何高风险越权执行触发安全门槛；修复并回归通过后方可答辩。
