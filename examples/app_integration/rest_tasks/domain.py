from __future__ import annotations

from threading import Lock
from typing import Any


class TaskStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._tasks: dict[int, dict[str, Any]] = {}
        self._next_id = 1

    def create(self, title: str) -> dict[str, Any]:
        normalized = title.strip()
        if not normalized or len(normalized) > 120:
            raise ValueError("title must contain 1..120 characters")
        with self._lock:
            item = {"id": self._next_id, "title": normalized, "done": False}
            self._tasks[self._next_id] = item
            self._next_id += 1
            return dict(item)

    def list(self) -> list[dict[str, Any]]:
        with self._lock:
            return [dict(self._tasks[key]) for key in sorted(self._tasks)]

    def complete(self, task_id: int) -> dict[str, Any]:
        with self._lock:
            if task_id not in self._tasks:
                raise KeyError(task_id)
            self._tasks[task_id]["done"] = True
            return dict(self._tasks[task_id])
