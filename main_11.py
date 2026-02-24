"""Level 11: MCP integration (Streamable HTTP server example)."""

import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp


async def main() -> None:
    # Start a local MCP server separately and update this URL as needed.
    mcp_url = "http://localhost:8000/mcp"

    try:
        async with MCPServerStreamableHttp(
            params={"url": mcp_url},
            cache_tools_list=True,
        ) as mcp_server:
            agent = Agent(
                name="MCPAssistant",
                instructions="Use MCP tools when they help answer accurately.",
                mcp_servers=[mcp_server],
            )
            result = await Runner.run(agent, "What tools do you have access to?")
            print(result.final_output)
    except Exception as exc:
        print("MCP demo could not run.")
        print("Reason:", exc)
        print("Tip: ensure an MCP server is running at", mcp_url)


if __name__ == "__main__":
    asyncio.run(main())

