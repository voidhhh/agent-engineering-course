# Agent 工程原理与 Harness 实战

一门从底层机制出发、兼顾原理解构与工程实践的中文课程。课程按照以下依赖关系展开：

`Model Output → Tool Calling → Agent Loop → MCP → Skill → Framework → Harness → Hermes / OpenClaw / DeepSeek Harness → Evals`

课程不是产品安装手册。学习者会先亲手实现最小 Agent Loop 和 Mini Harness，再使用同一组工具、Skill 与评测任务分析具体系统，从而区分模型能力、协议能力和运行时能力。

## 课程规格

- 16 讲，共 64 学时；每讲建议 2 学时原理、2 学时实验。
- 先修知识：Python、Git、Linux 命令行、HTTP/JSON、Docker 基础。
- 连续实验：本地“知识与任务助理”，数据仅使用 Markdown、JSON 和 SQLite。
- 期中项目：实现具备状态、审批、事件和恢复能力的 Mini Harness。
- 期末项目：在多种运行实现上执行同一评测集，并完成可复现的横向分析。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
python scripts/validate_course.py
agent-course-demo
```

默认测试使用确定性的 `ScriptedModel`，不需要 API Key，也不会访问网络。MCP、OpenAI Agents SDK、Hermes Agent、OpenClaw 和 DeepSeek Harness 实验均为可选扩展，按各实验说明单独安装。

MCP 进阶部分包含三种自研应用 Adapter：REST 任务软件、Qt 桌面笔记软件和 CLI 报告软件。安装 MCP 可选依赖后，可一次性运行无外部服务的端到端 Smoke Test：

```bash
python -m pip install -e ".[dev,mcp]"
python -m examples.app_integration.smoke
```

## 导航

- [课程大纲](syllabus/course-outline.md)
- [教学实施指南](syllabus/teaching-guide.md)
- [考核方案](syllabus/assessment.md)
- [课程技术基线](COURSE_BASELINE.md)
- [16 讲讲义](lectures/README.md)
- [实验手册](labs/README.md)
- [MCP 调用自研应用实例](examples/app_integration/README.md)
- [幻灯片讲稿](slides/README.md)
- [官方资料索引](references/official-reading-list.md)
- [评测说明](evals/README.md)
- [期中项目](midterm/README.md)
- [期末项目](capstone/README.md)
- [教师备课检查表](instructor/checklist.md)

## 仓库结构

```text
agent-engineering-course/
├── syllabus/           # 大纲、教学实施、考核
├── lectures/           # 16 讲原理解构讲义
├── slides/             # 可用 Marp 渲染的幻灯片讲稿
├── labs/               # 实验任务、平台接入与验收标准
├── src/agent_course/   # 可运行 Mini Harness
├── tests/              # 单元测试与失效机制测试
├── examples/           # MCP、Skill、平台配置示例
├── evals/              # 功能、安全与恢复评测集
├── quizzes/            # 模块测验与答案
├── midterm/            # 期中项目
├── capstone/           # 期末综合项目
├── instructor/         # 教师指南
└── scripts/            # 课程完整性检查
```

## 教学原则

1. **先重建，再使用。** 每个抽象都先用最小实现证明其必要性。
2. **同一任务，逐层升级。** 避免因不断更换 Demo 而混淆变量。
3. **失败路径是一等内容。** 超时、重复调用、越权、上下文膨胀和中断恢复都必须进入实验。
4. **固定版本，记录证据。** 具体产品实验应记录版本、配置、任务集、原始轨迹与评分脚本。
5. **区分事实、项目主张和实验结论。** 不用宣传语代替可复现实验。

## 授权说明

仓库暂未附加开源许可证。正式公开发布前，应由仓库所有者选择适用于代码与课程内容的授权方式。
