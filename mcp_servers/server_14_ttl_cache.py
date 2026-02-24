"""14 Advanced: TTL cache wrapper around expensive computation."""

import time
from hashlib import sha256

from _compat import MCPServer

mcp = MCPServer("server-14-ttl-cache")

_cache: dict[str, dict] = {}
TTL_SECONDS = 30


def _key(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


@mcp.tool()
def expensive_summary(text: str) -> dict:
    key = _key(text)
    now = time.time()
    if key in _cache and _cache[key]["expires_at"] > now:
        return {"cached": True, "summary": _cache[key]["value"]}

    words = [w for w in text.split() if w]
    summary = {
        "word_count": len(words),
        "first_10_words": " ".join(words[:10]),
        "last_10_words": " ".join(words[-10:]) if words else "",
    }
    _cache[key] = {"value": summary, "expires_at": now + TTL_SECONDS}
    return {"cached": False, "summary": summary}


@mcp.tool()
def cache_stats() -> dict:
    now = time.time()
    alive = sum(1 for value in _cache.values() if value["expires_at"] > now)
    return {"entries_total": len(_cache), "entries_alive": alive, "ttl_seconds": TTL_SECONDS}


if __name__ == "__main__":
    mcp.run(transport="stdio")

