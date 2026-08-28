from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from mcp.server import MCPServer

from examples.app_integration.cli_reports.bridge import ReportApplicationClient

mcp = MCPServer("course-cli-report-adapter")


def application_client() -> ReportApplicationClient:
    return ReportApplicationClient(
        Path(os.environ.get("COURSE_REPORT_DIR", "/tmp/agent-course-reports"))
    )


@mcp.tool()
def generate_local_report(
    title: str, rows: list[dict[str, str | float]], filename: str
) -> dict[str, Any]:
    """Generate one Markdown report in the configured local report workspace."""

    return application_client().generate(title, rows, filename)


@mcp.tool()
def list_local_reports() -> list[str]:
    """List report filenames in the configured local report workspace."""

    return application_client().list()


@mcp.tool()
def read_local_report(filename: str) -> str:
    """Read one validated Markdown report from the configured local workspace."""

    return application_client().read(filename)


if __name__ == "__main__":
    mcp.run(transport="stdio")
