"""Minimal OpenAI Agents SDK mapping for lecture 8.

This optional example makes a network model call and requires OPENAI_API_KEY.
The offline Mini Harness and its tests do not require a key.
"""

from __future__ import annotations

import os

from agents import Agent, Runner, function_tool

TASKS: list[str] = []


@function_tool
def add_task(title: str) -> str:
    """Create one in-memory teaching task after confirming the title is non-empty."""

    normalized = title.strip()
    if not normalized:
        raise ValueError("title must not be blank")
    TASKS.append(normalized)
    return f"created task {len(TASKS)}: {normalized}"


agent = Agent(
    name="Local task assistant",
    instructions=(
        "Help with the local teaching task list. Use add_task only when the user "
        "explicitly asks to create a task. Never claim an external action occurred."
    ),
    tools=[add_task],
)


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY for this optional online example.")
    result = Runner.run_sync(agent, "Create a task to inspect the agent trace")
    print(result.final_output)


if __name__ == "__main__":
    main()
