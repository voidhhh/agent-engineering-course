# 实例 B：MCP 调用自研 Qt 桌面笔记软件

数据流：`MCP Host → stdio MCP Adapter → loopback REST Control API → NoteStore → Qt UI Signal`。HTTP 请求在线程池处理，Qt 控件只在主线程更新；MCP Adapter 不直接操纵 GUI 对象。

## 安装与启动

```bash
python -m pip install -e ".[mcp,qt]"
export COURSE_APP_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(24))')"
python -m examples.app_integration.qt_notes.qt_app
```

在同样设置令牌的 MCP Host 配置中使用：

```bash
python -m examples.app_integration.qt_notes.mcp_server
```

Agent 可以检查应用、创建/列出笔记，并让指定笔记在桌面窗口中获得焦点。

## 为什么不用“让模型点击坐标”

应用控制 API 提供稳定、强类型、可测试的语义动作；像素坐标受窗口位置、缩放和主题影响，且难以做业务授权。需要视觉操作时仍可另建 Computer Use 实验，但不应替代应用原生接口。

## 安全边界

API 只监听 loopback、要求 Bearer Token、限制请求和字段长度；写入与窗口聚焦应在 Host 中分级。生产应用还需进程身份、令牌轮换、审计和用户可见控制面。
