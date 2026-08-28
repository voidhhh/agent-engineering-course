"""Start the example stdio server and call it through an MCP client session."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters


async def main() -> None:
    server = Path(__file__).with_name("task_server.py")
    parameters = StdioServerParameters(command=sys.executable, args=[str(server)])
    async with Client(parameters) as client:
        listed = await client.list_tools()
        print("tools:", [tool.name for tool in listed.tools])
        created = await client.call_tool("add_task", {"title": "trace MCP flow"})
        print("created:", created.content)
        tasks = await client.read_resource("tasks://all")
        print("resource:", tasks.contents)


if __name__ == "__main__":
    asyncio.run(main())
