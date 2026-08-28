from __future__ import annotations

from typing import Any

from examples.app_integration.common.json_http import request_json


class QtNotesClient:
    def __init__(self, base_url: str, token: str, timeout: float = 3.0) -> None:
        self.base_url = base_url
        self.token = token
        self.timeout = timeout

    def health(self) -> dict[str, Any]:
        return request_json(self.base_url, self.token, "GET", "/health", timeout=self.timeout)

    def create_note(self, title: str, body: str) -> dict[str, Any]:
        return request_json(
            self.base_url,
            self.token,
            "POST",
            "/notes",
            {"title": title, "body": body},
            self.timeout,
        )

    def list_notes(self) -> list[dict[str, Any]]:
        result = request_json(
            self.base_url, self.token, "GET", "/notes", timeout=self.timeout
        )
        return result["notes"]

    def focus_note(self, note_id: int) -> dict[str, Any]:
        return request_json(
            self.base_url,
            self.token,
            "POST",
            f"/notes/{note_id}/focus",
            {},
            self.timeout,
        )
