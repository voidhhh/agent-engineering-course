from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

from .models import ToolCall


@dataclass
class SessionState:
    session_id: str
    messages: list[dict[str, Any]] = field(default_factory=list)
    status: str = "ready"
    steps: int = 0
    pending_calls: list[ToolCall] = field(default_factory=list)
    last_error: str | None = None


class InMemorySessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, SessionState] = {}

    def create(self, session_id: str) -> SessionState:
        if session_id in self._sessions:
            raise ValueError(f"session already exists: {session_id}")
        state = SessionState(session_id=session_id)
        self.save(state)
        return state

    def get(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            raise KeyError(f"unknown session: {session_id}")
        return deepcopy(self._sessions[session_id])

    def save(self, state: SessionState) -> None:
        self._sessions[state.session_id] = deepcopy(state)
