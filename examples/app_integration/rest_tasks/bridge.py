from __future__ import annotations

from typing import Any

from examples.app_integration.common.json_http import request_json


class TaskApplicationClient:
    def __init__(self, base_url: str, token: str, timeout: float = 3.0) -> None:
        self.base_url = base_url
        self.token = token
        self.timeout = timeout

    def health(self) -> dict[str, Any]:
        return request_json(self.base_url, self.token, "GET", "/health", timeout=self.timeout)

    def create_task(self, title: str) -> dict[str, Any]:
        return request_json(
            self.base_url,
            self.token,
            "POST",
            "/tasks",
            {"title": title},
            self.timeout,
        )

    def list_tasks(self) -> list[dict[str, Any]]:
        result = request_json(
            self.base_url, self.token, "GET", "/tasks", timeout=self.timeout
        )
        return result["tasks"]

    def complete_task(self, task_id: int) -> dict[str, Any]:
        return request_json(
            self.base_url,
            self.token,
            "POST",
            f"/tasks/{task_id}/complete",
            {},
            self.timeout,
        )
