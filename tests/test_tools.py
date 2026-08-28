import pytest

from agent_course.tools import (
    ToolRegistry,
    ToolSpec,
    ToolValidationError,
    validate_arguments,
)

SCHEMA = {
    "type": "object",
    "properties": {"title": {"type": "string"}},
    "required": ["title"],
    "additionalProperties": False,
}


def test_argument_validation_rejects_missing_and_unknown_fields() -> None:
    with pytest.raises(ToolValidationError, match="missing required"):
        validate_arguments(SCHEMA, {})
    with pytest.raises(ToolValidationError, match="unknown arguments"):
        validate_arguments(SCHEMA, {"title": "x", "secret": "y"})


def test_registry_reuses_result_for_same_call_id() -> None:
    calls = 0

    def handler(args: dict[str, object]) -> dict[str, object]:
        nonlocal calls
        calls += 1
        return args

    registry = ToolRegistry()
    registry.register(ToolSpec("save", "Save value", SCHEMA, handler, risk="write"))
    first, first_reused = registry.execute("call-1", "save", {"title": "learn MCP"})
    second, second_reused = registry.execute("call-1", "save", {"title": "ignored"})

    assert first == second == {"title": "learn MCP"}
    assert first_reused is False
    assert second_reused is True
    assert calls == 1
