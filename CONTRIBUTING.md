# 贡献指南

课程内容修改需要同时考虑“讲义—实验—测试—评测”四个表面。

## 修改原则

- 原理性结论优先引用官方文档、官方仓库或论文。
- 快速演进项目必须注明核对日期和版本。
- 新实验必须提供目标、前置条件、步骤、验收标准和清理方式。
- 涉及外部 API 的实验应提供离线替身或清晰的跳过条件。
- 不提交密钥、真实个人数据、会话记录或未脱敏轨迹。

## 本地检查

```bash
python -m pip install -e ".[dev]"
ruff check src tests scripts
pytest
python scripts/validate_course.py
```
