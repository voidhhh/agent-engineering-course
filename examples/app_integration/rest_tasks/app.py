from __future__ import annotations

import argparse
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlsplit

from examples.app_integration.common.http_server import (
    LocalApplicationServer,
    is_authorized,
    read_json,
    send_json,
)
from examples.app_integration.rest_tasks.domain import TaskStore


def make_handler(store: TaskStore, token: str) -> type[BaseHTTPRequestHandler]:
    class TaskHandler(BaseHTTPRequestHandler):
        server_version = "CourseTaskApp/1.0"

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
                send_json(self, 200, {"status": "ok", "application": "course-task-app"})
            elif path == "/tasks":
                send_json(self, 200, {"tasks": store.list()})
            else:
                send_json(self, 404, {"error": "not found"})

        def do_POST(self) -> None:
            if not self._authorize():
                return
            path = urlsplit(self.path).path
            try:
                if path == "/tasks":
                    payload = read_json(self)
                    send_json(self, 201, store.create(str(payload.get("title", ""))))
                    return
                parts = path.strip("/").split("/")
                if len(parts) == 3 and parts[0] == "tasks" and parts[2] == "complete":
                    send_json(self, 200, store.complete(int(parts[1])))
                    return
                send_json(self, 404, {"error": "not found"})
            except (TypeError, ValueError) as exc:
                send_json(self, 400, {"error": str(exc)})
            except KeyError:
                send_json(self, 404, {"error": "task not found"})

    return TaskHandler


def build_server(
    host: str, port: int, token: str, store: TaskStore | None = None
) -> tuple[LocalApplicationServer, TaskStore]:
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("course application must bind to loopback")
    if not token:
        raise ValueError("COURSE_APP_TOKEN must not be empty")
    actual_store = store or TaskStore()
    return LocalApplicationServer((host, port), make_handler(actual_store, token)), actual_store


def main() -> None:
    parser = argparse.ArgumentParser(description="Local teaching task REST application")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    token = os.environ.get("COURSE_APP_TOKEN", "")
    server, _store = build_server(args.host, args.port, token)
    print(f"task application listening on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
