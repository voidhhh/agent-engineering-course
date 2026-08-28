from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples/skills/research-brief/scripts/validate_brief.py"


def load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("research_brief_validator", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_valid_research_brief() -> None:
    validator = load_validator()
    brief = """# Research Brief

## Scope
This brief compares two bounded approaches with a clear time boundary and question.

## Findings
The available primary evidence supports one finding, while a second remains uncertain.
The distinction is preserved and the supporting source appears below for verification.

## Sources
- [Primary source](https://example.com/evidence)

## Limitations
The sample is small, the evidence may become stale, and no causal claim is made.
"""
    assert validator.validate(brief) == []


def test_missing_sources_fail() -> None:
    validator = load_validator()
    errors = validator.validate("## Scope\nA\n## Findings\nB\n## Limitations\nC")
    assert "missing heading: ## Sources" in errors
