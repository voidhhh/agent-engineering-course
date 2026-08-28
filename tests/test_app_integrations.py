from __future__ import annotations

from pathlib import Path
from threading import Thread

import pytest

from examples.app_integration.cli_reports.bridge import (
    ReportApplicationClient,
    ReportApplicationError,
)
from examples.app_integration.common.json_http import ApplicationAPIError
from examples.app_integration.qt_notes.api import build_server as build_qt_server
from examples.app_integration.qt_notes.bridge import QtNotesClient
from examples.app_integration.qt_notes.domain import NoteStore
from examples.app_integration.rest_tasks.app import build_server as build_task_server
from examples.app_integration.rest_tasks.bridge import TaskApplicationClient


def start(server: object) -> Thread:
    thread = Thread(target=server.serve_forever, daemon=True)  # type: ignore[attr-defined]
    thread.start()
    return thread


def test_rest_task_application_roundtrip() -> None:
    server, _store = build_task_server("127.0.0.1", 0, "test-token")
    start(server)
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        client = TaskApplicationClient(base_url, "test-token")
        assert client.health()["status"] == "ok"
        created = client.create_task("integrate app")
        assert created["id"] == 1
        assert client.complete_task(1)["done"] is True
        assert client.list_tasks()[0]["title"] == "integrate app"
        with pytest.raises(ApplicationAPIError, match="401"):
            TaskApplicationClient(base_url, "wrong-token").list_tasks()
    finally:
        server.shutdown()
        server.server_close()


def test_qt_control_api_roundtrip_without_gui() -> None:
    store = NoteStore()
    changed: list[bool] = []
    focused: list[int] = []
    server = build_qt_server(
        "127.0.0.1",
        0,
        "test-token",
        store,
        on_changed=lambda: changed.append(True),
        on_focus=focused.append,
    )
    start(server)
    client = QtNotesClient(f"http://127.0.0.1:{server.server_address[1]}", "test-token")
    try:
        assert client.health()["status"] == "ok"
        assert client.create_note("Visible note", "Body")["id"] == 1
        assert client.list_notes()[0]["title"] == "Visible note"
        assert client.focus_note(1) == {"focused": 1}
        assert changed == [True]
        assert focused == [1]
    finally:
        server.shutdown()
        server.server_close()


def test_cli_report_application_is_confined(tmp_path: Path) -> None:
    client = ReportApplicationClient(tmp_path)
    result = client.generate(
        "Eval summary", [{"label": "passed", "value": 12}], "eval-summary.md"
    )
    assert result["row_count"] == 1
    assert client.list() == ["eval-summary.md"]
    assert "Total: 12" in client.read("eval-summary.md")
    with pytest.raises(ReportApplicationError, match="simple .md name"):
        client.generate("Escape", [{"label": "x", "value": 1}], "../escape.md")


def test_loopback_url_is_required() -> None:
    with pytest.raises(ValueError, match="loopback"):
        TaskApplicationClient("https://example.com", "token").health()
