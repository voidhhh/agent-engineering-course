from __future__ import annotations

import os
from typing import Any

from mcp.server import MCPServer

from examples.app_integration.rest_tasks.bridge import TaskApplicationClient

mcp = MCPServer("course-rest-task-adapter")


def application_client() -> TaskApplicationClient:
    return TaskApplicationClient(
        os.environ.get("COURSE_TASK_API", "http://127.0.0.1:8766"),
        os.environ.get("COURSE_APP_TOKEN", ""),
    )


@mcp.tool()
def task_app_health() -> dict[str, Any]:
    """Check whether the local course task application is reachable."""

    return application_client().health()


@mcp.tool()
def create_app_task(title: str) -> dict[str, Any]:
    """Create one task in the local course application. This changes application state."""

    return application_client().create_task(title)


@mcp.tool()
def list_app_tasks() -> list[dict[str, Any]]:
    """List tasks from the local course application without changing them."""

    return application_client().list_tasks()


@mcp.tool()
def complete_app_task(task_id: int) -> dict[str, Any]:
    """Mark one existing application task complete. This changes application state."""

    return application_client().complete_task(task_id)


if __name__ == "__main__":
    mcp.run(transport="stdio")
