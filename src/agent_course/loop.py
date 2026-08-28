from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .context import ContextBuilder
from .events import EventBus
from .models import ModelAdapter, ToolCall
from .policies import ApprovalDecision, StaticApprovalPolicy
from .sessions import InMemorySessionStore, SessionState
from .tools import ToolRegistry


@dataclass(frozen=True)
class RunResult:
    session_id: str
    status: str
    output: str | None
    pending_call_ids: tuple[str, ...] = ()
    error: str | None = None


class AgentLoop:
    def __init__(
        self,
        model: ModelAdapter,
        tools: ToolRegistry,
        sessions: InMemorySessionStore,
        events: EventBus,
        policy: StaticApprovalPolicy,
        context: ContextBuilder,
        max_steps: int = 8,
    ) -> None:
        self.model = model
        self.tools = tools
        self.sessions = sessions
        self.events = events
        self.policy = policy
        self.context = context
        self.max_steps = max_steps

    def start(self, session_id: str, user_input: str) -> RunResult:
        state = self.sessions.create(session_id)
        state.messages.append({"role": "user", "content": user_input})
        state.status = "running"
        self.sessions.save(state)
        self.events.emit("run.started", session_id, user_input=user_input)
        return self._advance(state)

    def resume(self, session_id: str, approved_call_ids: set[str]) -> RunResult:
        state = self.sessions.get(session_id)
        if state.status != "paused":
            raise ValueError(f"session is not paused: {session_id}")
        pending = list(state.pending_calls)
        state.pending_calls.clear()
        for call in pending:
            if call.id not in approved_call_ids:
                state.messages.append(self._tool_message(call, error="rejected by user"))
                self.events.emit("tool.rejected", session_id, call_id=call.id, tool=call.name)
                continue
            self._execute_call(state, call)
        state.status = "running"
        self.sessions.save(state)
        self.events.emit("run.resumed", session_id, approved=sorted(approved_call_ids))
        return self._advance(state)

    def _advance(self, state: SessionState) -> RunResult:
        while state.steps < self.max_steps:
            state.steps += 1
            self.events.emit("model.requested", state.session_id, step=state.steps)
            try:
                turn = self.model.complete(
                    self.context.build(state.messages), self.tools.schemas()
                )
            except Exception as exc:  # noqa: BLE001 - adapter boundary normalizes providers
                state.status = "failed"
                state.last_error = str(exc)
                self.sessions.save(state)
                self.events.emit("run.failed", state.session_id, error=str(exc))
                return RunResult(state.session_id, "failed", None, error=str(exc))

            self.events.emit(
                "model.responded",
                state.session_id,
                finish_reason=turn.finish_reason,
                tool_count=len(turn.tool_calls),
            )
            if turn.tool_calls:
                state.messages.append(
                    {
                        "role": "assistant",
                        "content": turn.content or "",
                        "tool_calls": [
                            {"id": call.id, "name": call.name, "arguments": call.arguments}
                            for call in turn.tool_calls
                        ],
                    }
                )
                pending: list[ToolCall] = []
                for call in turn.tool_calls:
                    try:
                        tool = self.tools.get(call.name)
                    except KeyError as exc:
                        state.messages.append(self._tool_message(call, error=str(exc)))
                        self.events.emit(
                            "tool.failed", state.session_id, call_id=call.id, error=str(exc)
                        )
                        continue
                    decision = self.policy.decide(call, tool)
                    self.events.emit(
                        "policy.decided",
                        state.session_id,
                        call_id=call.id,
                        tool=call.name,
                        decision=decision.value,
                    )
                    if decision is ApprovalDecision.DENY:
                        state.messages.append(self._tool_message(call, error="denied by policy"))
                    elif decision is ApprovalDecision.REQUIRE_APPROVAL:
                        pending.append(call)
                    else:
                        self._execute_call(state, call)
                if pending:
                    state.pending_calls = pending
                    state.status = "paused"
                    self.sessions.save(state)
                    self.events.emit(
                        "run.paused",
                        state.session_id,
                        pending=[call.id for call in pending],
                    )
                    return RunResult(
                        state.session_id,
                        "paused",
                        None,
                        pending_call_ids=tuple(call.id for call in pending),
                    )
                self.sessions.save(state)
                continue

            output = turn.content or ""
            state.messages.append({"role": "assistant", "content": output})
            state.status = "completed"
            self.sessions.save(state)
            self.events.emit("run.completed", state.session_id, output=output)
            return RunResult(state.session_id, "completed", output)

        state.status = "failed"
        state.last_error = "maximum step budget exceeded"
        self.sessions.save(state)
        self.events.emit("run.failed", state.session_id, error=state.last_error)
        return RunResult(state.session_id, "failed", None, error=state.last_error)

    def _execute_call(self, state: SessionState, call: ToolCall) -> None:
        self.events.emit("tool.started", state.session_id, call_id=call.id, tool=call.name)
        try:
            result, reused = self.tools.execute(call.id, call.name, call.arguments)
            state.messages.append(self._tool_message(call, result=result))
            self.events.emit(
                "tool.completed",
                state.session_id,
                call_id=call.id,
                tool=call.name,
                reused=reused,
                result=result,
            )
        except Exception as exc:  # noqa: BLE001 - tool boundary returns failures as observations
            state.messages.append(self._tool_message(call, error=str(exc)))
            self.events.emit(
                "tool.failed", state.session_id, call_id=call.id, tool=call.name, error=str(exc)
            )

    @staticmethod
    def _tool_message(
        call: ToolCall, result: Any | None = None, error: str | None = None
    ) -> dict[str, Any]:
        return {
            "role": "tool",
            "tool_call_id": call.id,
            "name": call.name,
            "content": {"ok": error is None, "result": result, "error": error},
        }
