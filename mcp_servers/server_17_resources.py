"""17 Advanced: MCP resources example."""

from datetime import datetime, timezone

from _compat import MCPServer

mcp = MCPServer("server-17-resources")


@mcp.resource("config://app")
def app_config() -> str:
    return "name=resource-demo\nenv=dev\nversion=1.0.0"


@mcp.resource("time://utc")
def utc_time() -> str:
    return datetime.now(timezone.utc).isoformat()


@mcp.resource("greeting://{name}")
def greeting_resource(name: str) -> str:
    return f"Hello from resource, {name}!"


if __name__ == "__main__":
    mcp.run(transport="stdio")

