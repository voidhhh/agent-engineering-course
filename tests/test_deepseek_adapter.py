from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from agent_course import DeepSeekChatAdapter, MiniHarness, ModelTurn, ScriptedModel, ToolCall
from agent_course.deepseek import DeepSeekConfigurationError, DeepSeekProtocolError
from agent_course.tools import build_course_tools


def ns(**values: Any) -> SimpleNamespace:
    return SimpleNamespace(**values)


class RecordingClient:
    def __init__(self, *responses: Any) -> None:
        self.responses = list(responses)
        self.requests: list[dict[str, Any]] = []
        self.chat = ns(completions=ns(create=self.create))

    def create(self, **request: Any) -> Any:
        self.requests.append(request)
        return self.responses.pop(0)


def response_with(*, message: Any, finish_reason: str = "stop") -> Any:
    return ns(
        choices=[ns(message=message, finish_reason=finish_reason)],
        usage=ns(prompt_tokens=10, completion_tokens=5, total_tokens=15),
    )


def test_adapter_normalizes_tool_call_and_request_schema() -> None:
    tool_call = ns(
        id="call-1",
        function=ns(name="add_numbers", arguments='{"a": 2, "b": 5}'),
    )
    client = RecordingClient(
        response_with(
            message=ns(
                content="",
                reasoning_content="I should use the arithmetic tool.",
                tool_calls=[tool_call],
            ),
            finish_reason="tool_calls",
        )
    )
    adapter = DeepSeekChatAdapter(
        client=client,
        model="deepseek-v4-pro",
        thinking=True,
        reasoning_effort="high",
        initial_tool_choice="required",
    )

    turn = adapter.complete(
        [{"role": "user", "content": "2 + 5"}], build_course_tools().schemas()
    )

    assert turn.tool_calls == (ToolCall("call-1", "add_numbers", {"a": 2, "b": 5}),)
    assert turn.reasoning == "I should use the arithmetic tool."
    assert turn.usage == {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
    request = client.requests[0]
    assert request["model"] == "deepseek-v4-pro"
    assert request["extra_body"] == {"thinking": {"type": "enabled"}}
    assert request["reasoning_effort"] == "high"
    assert request["tool_choice"] == "required"
    assert request["tools"][0]["function"]["name"] == "add_numbers"


def test_adapter_round_trips_reasoning_and_serializes_tool_result() -> None:
    client = RecordingClient(
        response_with(message=ns(content="The result is 7.", reasoning_content=None, tool_calls=[]))
    )
    adapter = DeepSeekChatAdapter(client=client, thinking=True)
    tools = build_course_tools().schemas()

    adapter.complete(
        [
            {"role": "user", "content": "2 + 5"},
            {
                "role": "assistant",
                "content": "",
                "reasoning": "Use add_numbers.",
                "tool_calls": [
                    {"id": "call-1", "name": "add_numbers", "arguments": {"a": 2, "b": 5}}
                ],
            },
            {
                "role": "tool",
                "tool_call_id": "call-1",
                "name": "add_numbers",
                "content": {"ok": True, "result": 7, "error": None},
            },
        ],
        tools,
    )

    provider_messages = client.requests[0]["messages"]
    assert client.requests[0]["tool_choice"] == "auto"
    assert provider_messages[1]["reasoning_content"] == "Use add_numbers."
    assert provider_messages[1]["tool_calls"][0]["function"]["arguments"] == '{"a": 2, "b": 5}'
    assert provider_messages[2]["content"] == '{"error": null, "ok": true, "result": 7}'


def test_adapter_rejects_invalid_tool_argument_json() -> None:
    call = ns(id="bad", function=ns(name="add_numbers", arguments="not-json"))
    client = RecordingClient(
        response_with(message=ns(content="", reasoning_content=None, tool_calls=[call]))
    )
    adapter = DeepSeekChatAdapter(client=client)

    with pytest.raises(DeepSeekProtocolError, match="invalid JSON arguments"):
        adapter.complete([{"role": "user", "content": "add"}], [])


def test_real_client_rejects_missing_or_placeholder_key_before_import() -> None:
    with pytest.raises(DeepSeekConfigurationError, match="real key"):
        DeepSeekChatAdapter(api_key="replace-with-your-deepseek-api-key")


def test_loop_persists_normalized_reasoning_for_tool_round_trip() -> None:
    model = ScriptedModel(
        [
            ModelTurn(
                reasoning="Need arithmetic.",
                tool_calls=(ToolCall("c1", "add_numbers", {"a": 1, "b": 2}),),
                finish_reason="tool_calls",
            ),
            ModelTurn(content="3"),
        ]
    )
    harness = MiniHarness(model, build_course_tools())

    assert harness.run("reasoning", "1 + 2").output == "3"
    assert harness.session("reasoning").messages[1]["reasoning"] == "Need arithmetic."
