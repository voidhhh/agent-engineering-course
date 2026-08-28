"""Minimal course MCP server.

Run after installing the optional dependency:
    python -m pip install -e ".[mcp]"
    python examples/mcp/task_server.py

The process uses stdio as protocol transport. Never print diagnostics to stdout.
"""

from __future__ import annotations

import json

from mcp.server import MCPServer

mcp = MCPServer("course-task-server")
tasks: list[dict[str, object]] = []


@mcp.tool()
def add_task(title: str) -> dict[str, object]:
    """Create one local teaching task and return it."""

    normalized = title.strip()
    if not normalized:
        raise ValueError("title must not be blank")
    if len(normalized) > 120:
        raise ValueError("title must be at most 120 characters")
    task: dict[str, object] = {
        "id": len(tasks) + 1,
        "title": normalized,
        "done": False,
    }
    tasks.append(task)
    return dict(task)


@mcp.tool()
def list_tasks() -> list[dict[str, object]]:
    """List tasks created in this server process."""

    return [dict(task) for task in tasks]


@mcp.resource("tasks://all")
def tasks_resource() -> str:
    """Return the task list as a JSON resource."""

    return json.dumps(tasks, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")
