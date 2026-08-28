from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolCall:
    """A provider-neutral request from a model to invoke one tool."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class ModelTurn:
    """One normalized model response consumed by the Agent loop."""

    content: str | None = None
    reasoning: str | None = None
    tool_calls: tuple[ToolCall, ...] = field(default_factory=tuple)
    finish_reason: str = "stop"
    usage: dict[str, int] = field(default_factory=dict)


class ModelAdapter(Protocol):
    def complete(
        self,
        messages: Sequence[dict[str, Any]],
        tools: Sequence[dict[str, Any]],
    ) -> ModelTurn:
        """Return a provider-neutral turn."""


class ScriptedModel:
    """Deterministic offline model used by labs, tests, and failure injection."""

    def __init__(self, turns: Sequence[ModelTurn]) -> None:
        if not turns:
            raise ValueError("ScriptedModel requires at least one turn")
        self._turns = deque(turns)
        self.requests: list[dict[str, Any]] = []

    def complete(
        self,
        messages: Sequence[dict[str, Any]],
        tools: Sequence[dict[str, Any]],
    ) -> ModelTurn:
        self.requests.append({"messages": list(messages), "tools": list(tools)})
        if not self._turns:
            raise RuntimeError("Scripted model exhausted before the loop terminated")
        return self._turns.popleft()
