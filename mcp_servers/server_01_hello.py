"""01 Beginner: Hello + echo tools."""

from _compat import MCPServer

mcp = MCPServer("server-01-hello")


@mcp.tool()
def hello(name: str = "world") -> str:
    return f"Hello, {name}!"


@mcp.tool()
def echo(text: str) -> str:
    return text


if __name__ == "__main__":
    mcp.run(transport="stdio")

