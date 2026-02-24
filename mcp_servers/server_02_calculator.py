"""02 Beginner: Basic calculator MCP server."""

from _compat import MCPServer

mcp = MCPServer("server-02-calculator")


@mcp.tool()
def add(a: float, b: float) -> float:
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


if __name__ == "__main__":
    mcp.run(transport="stdio")

