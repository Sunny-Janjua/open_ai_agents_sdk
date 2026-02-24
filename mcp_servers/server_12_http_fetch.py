"""12 Intermediate: HTTP fetch with allowlist."""

import json
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from _compat import MCPServer

mcp = MCPServer("server-12-http-fetch")

ALLOWED_HOSTS = {"api.github.com", "httpbin.org"}


def _validate(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http/https URLs are allowed.")
    if parsed.netloc not in ALLOWED_HOSTS:
        raise ValueError(f"Host '{parsed.netloc}' is not in allowlist.")


@mcp.tool()
def fetch_json(url: str, timeout_seconds: int = 10) -> dict:
    _validate(url)
    req = Request(url, headers={"User-Agent": "mcp-server-12"})
    with urlopen(req, timeout=timeout_seconds) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body)


if __name__ == "__main__":
    mcp.run(transport="stdio")

