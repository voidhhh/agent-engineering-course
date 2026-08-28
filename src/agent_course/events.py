from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class Event:
    sequence: int
    kind: str
    session_id: str
    payload: dict[str, Any]
    timestamp: str


class EventBus:
    def __init__(self) -> None:
        self._events: list[Event] = []
        self._subscribers: list[Callable[[Event], None]] = []

    def subscribe(self, callback: Callable[[Event], None]) -> None:
        self._subscribers.append(callback)

    def emit(self, kind: str, session_id: str, **payload: Any) -> Event:
        event = Event(
            sequence=len(self._events) + 1,
            kind=kind,
            session_id=session_id,
            payload=payload,
            timestamp=datetime.now(UTC).isoformat(),
        )
        self._events.append(event)
        for callback in tuple(self._subscribers):
            callback(event)
        return event

    def for_session(self, session_id: str) -> list[Event]:
        return [event for event in self._events if event.session_id == session_id]
