"""08 Intermediate: File-backed notes key-value store."""

import json
from pathlib import Path

from _compat import MCPServer

mcp = MCPServer("server-08-notes-store")

DB_PATH = Path(__file__).with_name("notes_store.json")


def _load() -> dict[str, str]:
    if not DB_PATH.exists():
        return {}
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def _save(data: dict[str, str]) -> None:
    DB_PATH.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


@mcp.tool()
def set_note(key: str, value: str) -> dict:
    data = _load()
    data[key] = value
    _save(data)
    return {"saved": True, "key": key}


@mcp.tool()
def get_note(key: str) -> dict:
    data = _load()
    return {"key": key, "value": data.get(key)}


@mcp.tool()
def list_note_keys() -> list[str]:
    data = _load()
    return sorted(data.keys())


@mcp.tool()
def delete_note(key: str) -> dict:
    data = _load()
    existed = key in data
    if existed:
        del data[key]
        _save(data)
    return {"deleted": existed, "key": key}


if __name__ == "__main__":
    mcp.run(transport="stdio")

