from __future__ import annotations

from collections.abc import Callable
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlsplit

from examples.app_integration.common.http_server import (
    LocalApplicationServer,
    is_authorized,
    read_json,
    send_json,
)
from examples.app_integration.qt_notes.domain import NoteStore


def make_handler(
    store: NoteStore,
    token: str,
    on_changed: Callable[[], None] | None = None,
    on_focus: Callable[[int], None] | None = None,
) -> type[BaseHTTPRequestHandler]:
    changed = on_changed or (lambda: None)
    focus = on_focus or (lambda _note_id: None)

    class NoteHandler(BaseHTTPRequestHandler):
        server_version = "CourseQtNotes/1.0"

        def log_message(self, format: str, *args: object) -> None:
            return

        def _authorize(self) -> bool:
            if is_authorized(self, token):
                return True
            send_json(self, 401, {"error": "unauthorized"})
            return False

        def do_GET(self) -> None:
            if not self._authorize():
                return
            path = urlsplit(self.path).path
            if path == "/health":
                send_json(self, 200, {"status": "ok", "application": "course-qt-notes"})
            elif path == "/notes":
                send_json(self, 200, {"notes": store.list()})
            else:
                send_json(self, 404, {"error": "not found"})

        def do_POST(self) -> None:
            if not self._authorize():
                return
            path = urlsplit(self.path).path
            try:
                if path == "/notes":
                    payload = read_json(self)
                    note = store.create(
                        str(payload.get("title", "")), str(payload.get("body", ""))
                    )
                    changed()
                    send_json(self, 201, note)
                    return
                parts = path.strip("/").split("/")
                if len(parts) == 3 and parts[0] == "notes" and parts[2] == "focus":
                    note_id = int(parts[1])
                    if not store.exists(note_id):
                        send_json(self, 404, {"error": "note not found"})
                        return
                    focus(note_id)
                    send_json(self, 200, {"focused": note_id})
                    return
                send_json(self, 404, {"error": "not found"})
            except (TypeError, ValueError) as exc:
                send_json(self, 400, {"error": str(exc)})

    return NoteHandler


def build_server(
    host: str,
    port: int,
    token: str,
    store: NoteStore,
    on_changed: Callable[[], None] | None = None,
    on_focus: Callable[[int], None] | None = None,
) -> LocalApplicationServer:
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("Qt control API must bind to loopback")
    if not token:
        raise ValueError("COURSE_APP_TOKEN must not be empty")
    return LocalApplicationServer(
        (host, port), make_handler(store, token, on_changed, on_focus)
    )
