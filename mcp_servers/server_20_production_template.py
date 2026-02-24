"""20 Advanced: Production-style MCP server template."""

import logging
import os
import time
from typing import Any

from _compat import MCPServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("server-20")

mcp = MCPServer("server-20-production-template")

_metrics: dict[str, Any] = {
    "requests_total": 0,
    "errors_total": 0,
    "started_at": time.time(),
}


def _observe_call(success: bool) -> None:
    _metrics["requests_total"] += 1
    if not success:
        _metrics["errors_total"] += 1


@mcp.tool()
def health() -> dict:
    uptime = int(time.time() - float(_metrics["started_at"]))
    return {"status": "ok", "uptime_seconds": uptime}


@mcp.tool()
def metrics() -> dict:
    return dict(_metrics)


@mcp.tool()
def transform(payload: str, mode: str = "upper") -> dict:
    try:
        if mode == "upper":
            result = payload.upper()
        elif mode == "lower":
            result = payload.lower()
        elif mode == "title":
            result = payload.title()
        else:
            raise ValueError("mode must be one of: upper, lower, title")
        _observe_call(True)
        return {"mode": mode, "output": result}
    except Exception:
        _observe_call(False)
        raise


def main() -> None:
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    logger.info("Starting MCP server with transport=%s", transport)

    if transport == "streamable-http":
        host = os.getenv("MCP_HOST", "127.0.0.1")
        port = int(os.getenv("MCP_PORT", "8000"))
        mcp.run(transport="streamable-http", host=host, port=port)
    elif transport == "sse":
        host = os.getenv("MCP_HOST", "127.0.0.1")
        port = int(os.getenv("MCP_PORT", "8000"))
        mcp.run(transport="sse", host=host, port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

