from __future__ import annotations

import asyncio
import os
from tempfile import TemporaryDirectory
from threading import Thread
from typing import Any

from mcp import Client

from examples.app_integration.cli_reports import mcp_server as cli_mcp
from examples.app_integration.qt_notes import mcp_server as qt_mcp
from examples.app_integration.qt_notes.api import build_server as build_qt_server
from examples.app_integration.qt_notes.domain import NoteStore
from examples.app_integration.rest_tasks import mcp_server as rest_mcp
from examples.app_integration.rest_tasks.app import build_server as build_task_server


async def call_tool(server: Any, name: str, arguments: dict[str, Any]) -> None:
    async with Client(server) as client:
        result = await client.call_tool(name, arguments)
        if result.is_error:
            raise RuntimeError(f"MCP tool failed: {name}: {result.content}")
        print(f"{name}: {result.content}")


async def smoke() -> None:
    token = "ephemeral-smoke-token"
    task_server, _task_store = build_task_server("127.0.0.1", 0, token)
    note_store = NoteStore()
    focused: list[int] = []
    note_server = build_qt_server(
        "127.0.0.1", 0, token, note_store, on_focus=focused.append
    )
    task_thread = Thread(target=task_server.serve_forever, daemon=True)
    note_thread = Thread(target=note_server.serve_forever, daemon=True)
    task_thread.start()
    note_thread.start()

    old_values = {
        name: os.environ.get(name)
        for name in ["COURSE_APP_TOKEN", "COURSE_TASK_API", "COURSE_QT_API", "COURSE_REPORT_DIR"]
    }
    try:
        os.environ["COURSE_APP_TOKEN"] = token
        os.environ["COURSE_TASK_API"] = (
            f"http://127.0.0.1:{task_server.server_address[1]}"
        )
        os.environ["COURSE_QT_API"] = f"http://127.0.0.1:{note_server.server_address[1]}"
        with TemporaryDirectory(prefix="agent-course-reports-") as report_dir:
            os.environ["COURSE_REPORT_DIR"] = report_dir
            await call_tool(
                rest_mcp.mcp, "create_app_task", {"title": "MCP controls a REST app"}
            )
            await call_tool(
                qt_mcp.mcp,
                "create_qt_note",
                {"title": "MCP note", "body": "Created through the Qt control API"},
            )
            await call_tool(qt_mcp.mcp, "focus_qt_note", {"note_id": 1})
            await call_tool(
                cli_mcp.mcp,
                "generate_local_report",
                {
                    "title": "MCP application smoke",
                    "rows": [{"label": "passed", "value": 3}],
                    "filename": "smoke.md",
                },
            )
            if focused != [1]:
                raise RuntimeError(f"Qt focus callback mismatch: {focused}")
    finally:
        for name, value in old_values.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
        task_server.shutdown()
        task_server.server_close()
        note_server.shutdown()
        note_server.server_close()


def main() -> None:
    asyncio.run(smoke())


if __name__ == "__main__":
    main()
