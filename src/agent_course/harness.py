from __future__ import annotations

from .context import ContextBuilder
from .events import Event, EventBus
from .loop import AgentLoop, RunResult
from .models import ModelAdapter
from .policies import StaticApprovalPolicy
from .sessions import InMemorySessionStore, SessionState
from .tools import ToolRegistry


class MiniHarness:
    """Composition root for the course's inspectable Agent runtime."""

    def __init__(
        self,
        model: ModelAdapter,
        tools: ToolRegistry,
        policy: StaticApprovalPolicy | None = None,
        max_steps: int = 8,
        max_messages: int = 20,
    ) -> None:
        self.sessions = InMemorySessionStore()
        self.events = EventBus()
        self.policy = policy or StaticApprovalPolicy()
        self.loop = AgentLoop(
            model=model,
            tools=tools,
            sessions=self.sessions,
            events=self.events,
            policy=self.policy,
            context=ContextBuilder(max_messages=max_messages),
            max_steps=max_steps,
        )

    def run(self, session_id: str, user_input: str) -> RunResult:
        return self.loop.start(session_id, user_input)

    def resume(self, session_id: str, approved_call_ids: set[str]) -> RunResult:
        return self.loop.resume(session_id, approved_call_ids)

    def session(self, session_id: str) -> SessionState:
        return self.sessions.get(session_id)

    def trace(self, session_id: str) -> list[Event]:
        return self.events.for_session(session_id)
