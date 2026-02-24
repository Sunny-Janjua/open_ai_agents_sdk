"""16 Advanced: Token-guarded sensitive tools."""

import os
from datetime import datetime

from _compat import MCPServer

mcp = MCPServer("server-16-auth-guard")

API_TOKEN = os.getenv("MCP_SERVER16_TOKEN", "")


def _require_token(token: str) -> None:
    if not API_TOKEN:
        raise ValueError("Server token is not configured (MCP_SERVER16_TOKEN).")
    if token != API_TOKEN:
        raise ValueError("Invalid token.")


@mcp.tool()
def public_ping() -> str:
    return "pong"


@mcp.tool()
def sensitive_audit_log(token: str, message: str) -> dict:
    _require_token(token)
    return {"saved": True, "at": datetime.utcnow().isoformat() + "Z", "message": message}


if __name__ == "__main__":
    mcp.run(transport="stdio")

