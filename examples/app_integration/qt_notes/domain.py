from __future__ import annotations

from threading import Lock
from typing import Any


class NoteStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._notes: dict[int, dict[str, Any]] = {}
        self._next_id = 1

    def create(self, title: str, body: str) -> dict[str, Any]:
        normalized_title = title.strip()
        normalized_body = body.strip()
        if not normalized_title or len(normalized_title) > 100:
            raise ValueError("title must contain 1..100 characters")
        if len(normalized_body) > 10_000:
            raise ValueError("body must contain at most 10000 characters")
        with self._lock:
            note = {
                "id": self._next_id,
                "title": normalized_title,
                "body": normalized_body,
            }
            self._notes[self._next_id] = note
            self._next_id += 1
            return dict(note)

    def list(self) -> list[dict[str, Any]]:
        with self._lock:
            return [dict(self._notes[key]) for key in sorted(self._notes)]

    def exists(self, note_id: int) -> bool:
        with self._lock:
            return note_id in self._notes
