"""05 Beginner: JSON validate, pretty-print, merge."""

import json

from _compat import MCPServer

mcp = MCPServer("server-05-json-toolkit")


@mcp.tool()
def validate_json(payload: str) -> dict:
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        return {"valid": False, "error": str(exc)}
    return {"valid": True, "type": type(parsed).__name__}


@mcp.tool()
def pretty_json(payload: str) -> str:
    return json.dumps(json.loads(payload), indent=2, sort_keys=True)


@mcp.tool()
def merge_objects(base_json: str, override_json: str) -> str:
    base = json.loads(base_json)
    override = json.loads(override_json)
    if not isinstance(base, dict) or not isinstance(override, dict):
        raise ValueError("Both inputs must be JSON objects.")
    merged = {**base, **override}
    return json.dumps(merged, indent=2, sort_keys=True)


if __name__ == "__main__":
    mcp.run(transport="stdio")

