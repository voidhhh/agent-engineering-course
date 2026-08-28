"""Validate the minimum structure of a Markdown research brief."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = ("Scope", "Findings", "Sources", "Limitations")


def validate(text: str) -> list[str]:
    errors: list[str] = []
    for heading in REQUIRED_HEADINGS:
        if not re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE):
            errors.append(f"missing heading: ## {heading}")
    sources = re.search(
        r"^##\s+Sources\s*$([\s\S]*?)(?=^##\s+|\Z)", text, re.MULTILINE
    )
    if sources and not re.search(r"https?://|\[[^]]+\]\([^)]+\)", sources.group(1)):
        errors.append("Sources must contain at least one URL or Markdown link")
    if len(text.split()) < 40:
        errors.append("brief is too short to demonstrate evidence synthesis")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_brief.py BRIEF.md", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    errors = validate(path.read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"valid research brief: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
