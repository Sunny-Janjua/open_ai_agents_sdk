"""11 Intermediate: SQLite query server with guarded SQL."""

import sqlite3
from pathlib import Path

from _compat import MCPServer

mcp = MCPServer("server-11-sqlite-query")

DB_PATH = Path(__file__).with_name("server_11.db")


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@mcp.tool()
def init_db() -> dict:
    with _conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
            """
        )
    return {"ok": True}


@mcp.tool()
def add_user(name: str, email: str) -> dict:
    with _conn() as conn:
        cur = conn.execute("INSERT INTO users(name, email) VALUES(?, ?)", (name, email))
    return {"id": cur.lastrowid, "name": name, "email": email}


@mcp.tool()
def select_query(sql: str) -> list[dict]:
    text = sql.strip().lower()
    if not text.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    with _conn() as conn:
        rows = conn.execute(sql).fetchall()
    return [dict(r) for r in rows]


if __name__ == "__main__":
    mcp.run(transport="stdio")

