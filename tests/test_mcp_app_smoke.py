from __future__ import annotations

import asyncio

from examples.app_integration.smoke import smoke


def test_all_application_adapters_over_mcp() -> None:
    asyncio.run(smoke())
