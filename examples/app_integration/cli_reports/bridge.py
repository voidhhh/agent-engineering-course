from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class ReportApplicationError(RuntimeError):
    pass


class ReportApplicationClient:
    def __init__(self, workspace: Path, timeout: float = 5.0) -> None:
        self.workspace = workspace.resolve()
        self.timeout = timeout
        self.executable = Path(__file__).with_name("report_app.py")

    def request(self, payload: dict[str, Any]) -> Any:
        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(self.executable),
                    "--workspace",
                    str(self.workspace),
                ],
                input=json.dumps(payload),
                text=True,
                capture_output=True,
                timeout=self.timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise ReportApplicationError("report application timed out") from exc
        try:
            response = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise ReportApplicationError("report application returned invalid JSON") from exc
        if completed.returncode != 0 or not response.get("ok"):
            raise ReportApplicationError(response.get("error", "report application failed"))
        return response["result"]

    def generate(
        self, title: str, rows: list[dict[str, str | float]], filename: str
    ) -> dict[str, Any]:
        return self.request(
            {"operation": "generate", "title": title, "rows": rows, "filename": filename}
        )

    def list(self) -> list[str]:
        return self.request({"operation": "list"})["reports"]

    def read(self, filename: str) -> str:
        return self.request({"operation": "read", "filename": filename})["content"]
