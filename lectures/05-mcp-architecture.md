# 第 5 讲：MCP 协议架构

## 学习目标

理解 MCP Host、Client、Server 的关系、数据层与传输层、能力协商及三类核心 Server 能力。

## 1. MCP 解决什么

没有协议时，每个 Agent 与每个外部系统都需要专用适配器。MCP 使用 JSON-RPC 消息和能力发现，使 Host 能以统一方式连接工具与数据源。它降低连接成本，但不决定 Agent 策略，也不替代业务权限。

Host 是面向用户并拥有整体安全责任的应用。Host 通常为每个 Server 建立 Client 连接。Server 暴露能力，但不应假设收到请求就代表最终用户已授权所有行为。

## 2. 两层协议

数据层规定 JSON-RPC 消息、生命周期、能力和通知；传输层规定消息如何在进程或网络间移动。stdio 适合同机子进程，标准输出必须只承载协议帧，日志写入标准错误。Streamable HTTP 适合远程连接，可结合标准 HTTP 鉴权和流式事件。

## 3. 生命周期与能力协商

连接建立后，参与方协商协议版本和能力。客户端不能在未发现能力时假设 Server 支持某个操作。通知、进度和取消使长任务可以被观察与中止。

## 4. Tools、Resources、Prompts

- Tools：模型可能选择执行的动作；有副作用风险。
- Resources：通过 URI 标识的上下文数据；读取同样需要访问控制。
- Prompts：由 Server 提供的可参数化交互模板；更接近用户选择的工作流入口。

三者不能互相替代。把所有内容都暴露为 Tool 会增加工具目录和决策负担；把写操作伪装为 Resource 会模糊副作用。

## 5. 信任边界

Server 返回的工具描述、资源内容和错误消息都是外部输入，可能包含提示注入。Host 需要显示来源、过滤工具、限制参数、保护凭据并对敏感调用获得明确同意。MCP 是能力通道，不是沙箱。

## 实验

捕获一次 initialize、tools/list 和 tools/call 交换，标出 request id、method、params、result 和 error。解释协议版本不匹配、Server 无响应和工具 schema 改变时 Host 应如何处理。
