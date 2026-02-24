"""03 Beginner: Text utility tools."""

import re

from _compat import MCPServer

mcp = MCPServer("server-03-text-utils")


@mcp.tool()
def word_count(text: str) -> int:
    return len([w for w in text.strip().split() if w])


@mcp.tool()
def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    return slug.strip("-")


@mcp.tool()
def reverse_text(text: str) -> str:
    return text[::-1]


if __name__ == "__main__":
    mcp.run(transport="stdio")

