from __future__ import annotations

from .harness import MiniHarness
from .models import ModelTurn, ScriptedModel, ToolCall
from .tools import build_course_tools


def main() -> None:
    model = ScriptedModel(
        [
            ModelTurn(
                tool_calls=(
                    ToolCall("demo-call-1", "add_numbers", {"a": 17, "b": 25}),
                ),
                finish_reason="tool_calls",
            ),
            ModelTurn(content="17 + 25 = 42"),
        ]
    )
    harness = MiniHarness(model, build_course_tools())
    result = harness.run("demo", "计算 17 + 25")
    print(f"status: {result.status}")
    print(f"output: {result.output}")
    print("trace:")
    for event in harness.trace("demo"):
        print(f"  {event.sequence:02d} {event.kind} {event.payload}")


if __name__ == "__main__":
    main()
