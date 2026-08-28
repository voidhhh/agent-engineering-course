from agent_course import MiniHarness, ModelTurn, ScriptedModel, ToolCall
from agent_course.policies import StaticApprovalPolicy
from agent_course.tools import build_course_tools


def test_loop_executes_tool_and_finishes() -> None:
    model = ScriptedModel(
        [
            ModelTurn(
                tool_calls=(ToolCall("c1", "add_numbers", {"a": 2, "b": 5}),),
                finish_reason="tool_calls",
            ),
            ModelTurn(content="结果是 7"),
        ]
    )
    harness = MiniHarness(model, build_course_tools())

    result = harness.run("s1", "2 + 5 等于多少？")

    assert result.status == "completed"
    assert result.output == "结果是 7"
    kinds = [event.kind for event in harness.trace("s1")]
    assert kinds == [
        "run.started",
        "model.requested",
        "model.responded",
        "policy.decided",
        "tool.started",
        "tool.completed",
        "model.requested",
        "model.responded",
        "run.completed",
    ]
    responded = [
        event for event in harness.trace("s1") if event.kind == "model.responded"
    ]
    assert responded[0].payload["usage"] == {}


def test_write_tool_pauses_and_resumes_after_approval() -> None:
    model = ScriptedModel(
        [
            ModelTurn(
                tool_calls=(ToolCall("write-1", "add_task", {"title": "学习 Skill"}),),
                finish_reason="tool_calls",
            ),
            ModelTurn(content="任务已创建"),
        ]
    )
    harness = MiniHarness(model, build_course_tools())

    paused = harness.run("approval", "创建学习任务")
    assert paused.status == "paused"
    assert paused.pending_call_ids == ("write-1",)

    completed = harness.resume("approval", {"write-1"})
    assert completed.status == "completed"
    assert completed.output == "任务已创建"


def test_policy_denial_returns_error_to_model_without_execution() -> None:
    model = ScriptedModel(
        [
            ModelTurn(
                tool_calls=(ToolCall("deny-1", "add_task", {"title": "blocked"}),),
                finish_reason="tool_calls",
            ),
            ModelTurn(content="操作被策略拒绝"),
        ]
    )
    policy = StaticApprovalPolicy(denied_tools={"add_task"})
    harness = MiniHarness(model, build_course_tools(), policy=policy)

    result = harness.run("denied", "创建任务")

    assert result.status == "completed"
    assert harness.session("denied").messages[-2]["content"]["error"] == "denied by policy"


def test_step_budget_terminates_run() -> None:
    model = ScriptedModel(
        [
            ModelTurn(
                tool_calls=(ToolCall(f"c{i}", "list_tasks", {}),),
                finish_reason="tool_calls",
            )
            for i in range(3)
        ]
    )
    harness = MiniHarness(model, build_course_tools(), max_steps=2)

    result = harness.run("budget", "不断检查任务")

    assert result.status == "failed"
    assert result.error == "maximum step budget exceeded"
