from __future__ import annotations

import hmac
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


class LocalApplicationServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def is_authorized(handler: BaseHTTPRequestHandler, token: str) -> bool:
    supplied = handler.headers.get("Authorization", "")
    return hmac.compare_digest(supplied, f"Bearer {token}")


def read_json(handler: BaseHTTPRequestHandler, max_bytes: int = 65_536) -> dict[str, Any]:
    try:
        length = int(handler.headers.get("Content-Length", "0"))
    except ValueError as exc:
        raise ValueError("invalid Content-Length") from exc
    if length < 1 or length > max_bytes:
        raise ValueError(f"request body must contain 1..{max_bytes} bytes")
    try:
        item = json.loads(handler.rfile.read(length))
    except json.JSONDecodeError as exc:
        raise ValueError("request body must be valid JSON") from exc
    if not isinstance(item, dict):
        raise TypeError("request body must be a JSON object")
    return item


def send_json(handler: BaseHTTPRequestHandler, status: int, payload: Any) -> None:
    encoded = json.dumps(payload, ensure_ascii=False).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(encoded)))
    handler.end_headers()
    handler.wfile.write(encoded)
