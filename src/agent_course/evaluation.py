from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .harness import MiniHarness


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    prompt: str
    expected_status: str = "completed"
    expected_substring: str | None = None


@dataclass(frozen=True)
class EvalOutcome:
    case_id: str
    passed: bool
    status: str
    output: str | None
    reason: str


def evaluate(
    cases: list[EvalCase], harness_factory: Callable[[EvalCase], MiniHarness]
) -> list[EvalOutcome]:
    outcomes: list[EvalOutcome] = []
    for case in cases:
        harness = harness_factory(case)
        result = harness.run(case.case_id, case.prompt)
        status_ok = result.status == case.expected_status
        content_ok = case.expected_substring is None or (
            result.output is not None and case.expected_substring in result.output
        )
        passed = status_ok and content_ok
        reason = "ok" if passed else f"status={result.status}, output={result.output!r}"
        outcomes.append(
            EvalOutcome(case.case_id, passed, result.status, result.output, reason)
        )
    return outcomes
