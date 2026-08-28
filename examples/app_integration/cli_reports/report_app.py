from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

FILENAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}\.md$")


def safe_report_path(workspace: Path, filename: str) -> Path:
    if not FILENAME.fullmatch(filename):
        raise ValueError("filename must be a simple .md name without directories")
    workspace.mkdir(parents=True, exist_ok=True)
    root = workspace.resolve()
    if root == Path(root.anchor) or root == Path.home().resolve():
        raise ValueError("workspace is too broad")
    path = root / filename
    if path.parent != root:
        raise ValueError("report path leaves workspace")
    return path


def generate_report(workspace: Path, request: dict[str, Any]) -> dict[str, Any]:
    title = str(request.get("title", "")).strip()
    filename = str(request.get("filename", ""))
    rows = request.get("rows", [])
    if not title or len(title) > 120:
        raise ValueError("title must contain 1..120 characters")
    if not isinstance(rows, list) or not 1 <= len(rows) <= 100:
        raise ValueError("rows must contain 1..100 items")
    normalized: list[tuple[str, float]] = []
    for row in rows:
        if not isinstance(row, dict):
            raise TypeError("each row must be an object")
        label = str(row.get("label", "")).strip()
        value = row.get("value")
        if not label or len(label) > 80 or isinstance(value, bool) or not isinstance(
            value, (int, float)
        ):
            raise ValueError("each row needs a short label and numeric value")
        normalized.append((label.replace("|", "\\|"), float(value)))

    path = safe_report_path(workspace, filename)
    if path.exists() or path.is_symlink():
        raise FileExistsError(f"report already exists: {filename}")
    lines = [
        f"# {title}",
        "",
        "| Item | Value |",
        "|---|---:|",
        *[f"| {label} | {value:g} |" for label, value in normalized],
        "",
        f"Total: {sum(value for _label, value in normalized):g}",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return {"filename": filename, "row_count": len(normalized), "bytes": path.stat().st_size}


def list_reports(workspace: Path) -> dict[str, Any]:
    workspace.mkdir(parents=True, exist_ok=True)
    root = workspace.resolve()
    reports = [
        path.name
        for path in sorted(root.glob("*.md"))
        if path.is_file() and not path.is_symlink()
    ]
    return {"reports": reports}


def read_report(workspace: Path, filename: str) -> dict[str, Any]:
    path = safe_report_path(workspace, filename)
    if not path.is_file() or path.is_symlink():
        raise FileNotFoundError(filename)
    if path.stat().st_size > 100_000:
        raise ValueError("report exceeds 100 KB")
    return {"filename": filename, "content": path.read_text(encoding="utf-8")}


def dispatch(workspace: Path, request: dict[str, Any]) -> dict[str, Any]:
    operation = request.get("operation")
    if operation == "generate":
        return generate_report(workspace, request)
    if operation == "list":
        return list_reports(workspace)
    if operation == "read":
        return read_report(workspace, str(request.get("filename", "")))
    raise ValueError(f"unsupported operation: {operation!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Restricted local report application")
    parser.add_argument("--workspace", required=True, type=Path)
    args = parser.parse_args()
    try:
        raw = sys.stdin.read(65_537)
        if len(raw) > 65_536:
            raise ValueError("request exceeds 64 KB")
        request = json.loads(raw)
        if not isinstance(request, dict):
            raise TypeError("request must be a JSON object")
        response = {"ok": True, "result": dispatch(args.workspace, request)}
    except (
        FileExistsError,
        FileNotFoundError,
        TypeError,
        json.JSONDecodeError,
        ValueError,
    ) as exc:
        response = {"ok": False, "error": str(exc)}
    print(json.dumps(response, ensure_ascii=False))
    return 0 if response["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
