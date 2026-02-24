"""15 Advanced: Simple per-client rate limiter."""

import time

from _compat import MCPServer

mcp = MCPServer("server-15-rate-limit")

WINDOW_SECONDS = 60
MAX_REQUESTS = 5
_hits: dict[str, list[float]] = {}


def _check_limit(client_id: str) -> None:
    now = time.time()
    window_start = now - WINDOW_SECONDS
    _hits.setdefault(client_id, [])
    _hits[client_id] = [t for t in _hits[client_id] if t >= window_start]
    if len(_hits[client_id]) >= MAX_REQUESTS:
        raise ValueError("Rate limit exceeded. Try again later.")
    _hits[client_id].append(now)


@mcp.tool()
def limited_echo(client_id: str, message: str) -> dict:
    _check_limit(client_id)
    return {"client_id": client_id, "message": message}


@mcp.tool()
def rate_limit_config() -> dict:
    return {"window_seconds": WINDOW_SECONDS, "max_requests": MAX_REQUESTS}


if __name__ == "__main__":
    mcp.run(transport="stdio")

