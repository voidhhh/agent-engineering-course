from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(path: str) -> None:
    full = ROOT / path
    if not full.exists():
        raise SystemExit(f"missing required course artifact: {path}")


def validate_jsonl(path: str, expected_category: str, seen_ids: set[str]) -> int:
    full = ROOT / path
    count = 0
    with full.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"invalid JSONL at {path}:{line_number}: {exc}") from exc
            if "id" not in item or "prompt" not in item:
                raise SystemExit(f"JSONL item lacks id/prompt at {path}:{line_number}")
            if item["id"] in seen_ids:
                raise SystemExit(f"duplicate eval id at {path}:{line_number}: {item['id']}")
            if item.get("category") != expected_category:
                raise SystemExit(
                    f"wrong category at {path}:{line_number}: "
                    f"expected {expected_category}, got {item.get('category')!r}"
                )
            if not isinstance(item.get("max_steps"), int) or item["max_steps"] < 1:
                raise SystemExit(f"invalid max_steps at {path}:{line_number}")
            seen_ids.add(item["id"])
            count += 1
    return count


def validate_local_links() -> None:
    pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for markdown in ROOT.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for raw_target in pattern.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (markdown.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError as exc:
                raise SystemExit(
                    f"local link leaves repository: {markdown.relative_to(ROOT)} -> {target}"
                ) from exc
            if not resolved.exists():
                raise SystemExit(
                    f"broken local link: {markdown.relative_to(ROOT)} -> {target}"
                )


def validate_live_api_safety() -> None:
    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    expected = "DEEPSEEK_API_KEY=replace-with-your-deepseek-api-key"
    if expected not in env_example:
        raise SystemExit(".env.example must contain only the documented DeepSeek key placeholder")

    ignore_entries = {
        line.strip()
        for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    if ".env" not in ignore_entries:
        raise SystemExit(".gitignore must ignore .env before live API labs are enabled")


def main() -> None:
    required = [
        "README.md",
        ".env.example",
        "COURSE_BASELINE.md",
        "syllabus/course-outline.md",
        "syllabus/teaching-guide.md",
        "syllabus/assessment.md",
        "lectures/README.md",
        "slides/README.md",
        "labs/README.md",
        "labs/02b-mcp-app-integration.md",
        "labs/01b-deepseek-api.md",
        "references/official-reading-list.md",
        "examples/app_integration/README.md",
        "examples/app_integration/rest_tasks/app.py",
        "examples/app_integration/rest_tasks/mcp_server.py",
        "examples/app_integration/qt_notes/qt_app.py",
        "examples/app_integration/qt_notes/mcp_server.py",
        "examples/app_integration/cli_reports/report_app.py",
        "examples/app_integration/cli_reports/mcp_server.py",
        "examples/deepseek_api/README.md",
        "examples/deepseek_api/demo.py",
        "src/agent_course/deepseek.py",
        "tests/test_deepseek_adapter.py",
        "tests/test_deepseek_live.py",
        "quizzes/module-quizzes.md",
        "quizzes/answer-key.md",
        "midterm/README.md",
        "capstone/README.md",
        "evals/functional.jsonl",
        "evals/security.jsonl",
        "evals/resilience.jsonl",
    ]
    for path in required:
        require(path)
    lectures = sorted((ROOT / "lectures").glob("[0-9][0-9]-*.md"))
    slides = sorted((ROOT / "slides").glob("[0-9][0-9]-*.md"))
    if len(lectures) != 16:
        raise SystemExit(f"expected 16 lecture files, found {len(lectures)}")
    if len(slides) != 16:
        raise SystemExit(f"expected 16 slide files, found {len(slides)}")
    seen_ids: set[str] = set()
    eval_sets = [
        ("evals/functional.jsonl", "functional"),
        ("evals/security.jsonl", "security"),
        ("evals/resilience.jsonl", "resilience"),
    ]
    counts = {
        category: validate_jsonl(path, category, seen_ids)
        for path, category in eval_sets
    }
    if any(count < 10 for count in counts.values()):
        raise SystemExit(f"expected at least 10 eval cases per category, found {counts}")
    total_cases = sum(counts.values())
    if total_cases < 30:
        raise SystemExit(f"expected at least 30 eval cases, found {total_cases}")
    validate_local_links()
    validate_live_api_safety()
    print(f"course validation passed: 16 lectures, 16 decks, {total_cases} eval cases")


if __name__ == "__main__":
    main()
