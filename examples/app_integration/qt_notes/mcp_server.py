from __future__ import annotations

import os
from typing import Any

from mcp.server import MCPServer

from examples.app_integration.qt_notes.bridge import QtNotesClient

mcp = MCPServer("course-qt-notes-adapter")


def application_client() -> QtNotesClient:
    port = os.environ.get("COURSE_QT_PORT", "8767")
    return QtNotesClient(
        os.environ.get("COURSE_QT_API", f"http://127.0.0.1:{port}"),
        os.environ.get("COURSE_APP_TOKEN", ""),
    )


@mcp.tool()
def qt_notes_health() -> dict[str, Any]:
    """Check whether the local Qt Notes application control API is reachable."""

    return application_client().health()


@mcp.tool()
def create_qt_note(title: str, body: str) -> dict[str, Any]:
    """Create a note inside the visible local Qt application. This changes app state."""

    return application_client().create_note(title, body)


@mcp.tool()
def list_qt_notes() -> list[dict[str, Any]]:
    """List notes currently held by the local Qt application."""

    return application_client().list_notes()


@mcp.tool()
def focus_qt_note(note_id: int) -> dict[str, Any]:
    """Bring an existing note into focus in the visible Qt application."""

    return application_client().focus_note(note_id)


if __name__ == "__main__":
    mcp.run(transport="stdio")
