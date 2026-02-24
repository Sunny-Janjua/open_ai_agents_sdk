"""04 Beginner: Date and time helpers."""

from datetime import datetime
from zoneinfo import ZoneInfo

from _compat import MCPServer

mcp = MCPServer("server-04-datetime")


@mcp.tool()
def now_utc() -> str:
    return datetime.now(tz=ZoneInfo("UTC")).isoformat()


@mcp.tool()
def now_in_timezone(tz_name: str) -> str:
    return datetime.now(tz=ZoneInfo(tz_name)).isoformat()


@mcp.tool()
def date_diff_days(date_a: str, date_b: str) -> int:
    a = datetime.fromisoformat(date_a)
    b = datetime.fromisoformat(date_b)
    return abs((a - b).days)


if __name__ == "__main__":
    mcp.run(transport="stdio")

