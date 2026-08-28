from agent_course import MiniHarness, ModelTurn, ScriptedModel
from agent_course.evaluation import EvalCase, evaluate
from agent_course.tools import build_course_tools


def test_eval_runner_scores_expected_content() -> None:
    cases = [EvalCase("case-1", "say ready", expected_substring="ready")]

    def factory(_case: EvalCase) -> MiniHarness:
        return MiniHarness(ScriptedModel([ModelTurn(content="ready")]), build_course_tools())

    outcomes = evaluate(cases, factory)

    assert outcomes[0].passed is True
    assert outcomes[0].reason == "ok"
