from __future__ import annotations

from collections.abc import Sequence
from typing import Any


class ContextBuilder:
    """Build bounded model-visible context while keeping tool-result adjacency."""

    def __init__(self, max_messages: int = 20) -> None:
        if max_messages < 4:
            raise ValueError("max_messages must be at least 4")
        self.max_messages = max_messages

    def build(self, messages: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
        if len(messages) <= self.max_messages:
            return [dict(item) for item in messages]
        removed = len(messages) - (self.max_messages - 1)
        summary = {
            "role": "system",
            "content": f"[context compacted: {removed} earlier messages omitted]",
        }
        return [summary, *[dict(item) for item in messages[-(self.max_messages - 1) :]]]
