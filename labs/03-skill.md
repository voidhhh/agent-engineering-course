# 实验 03：设计与评测 Agent Skill

## 目标

把“如何形成研究简报”的程序性知识做成按需加载、可验证的 Skill。

## 任务

1. 阅读 `examples/skills/research-brief/SKILL.md`；
2. 检查 frontmatter 的 `description` 是否同时覆盖能力与触发场景；
3. 把详细质量标准保留在 `references/checklist.md`，避免与正文重复；
4. 运行校验脚本：

```bash
python examples/skills/research-brief/scripts/validate_brief.py sample.md
```

5. 设计至少 12 个 Eval：4 个应触发、4 个不应触发、2 个资料不足、2 个恶意资料；
6. 记录未使用 Skill 与使用 Skill 时的格式、事实和 Token 差异。

## 验收

- Skill 主体只包含核心工作流；
- 参考资料仅在任务需要时读取；
- 校验脚本真实运行并能产生非零失败码；
- 不应触发的请求不会错误加载 Skill；
- 外部资料中的指令不会覆盖用户任务和安全策略。
