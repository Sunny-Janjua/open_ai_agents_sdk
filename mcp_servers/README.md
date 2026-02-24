# 20 MCP Servers: Beginner to Advanced

This folder contains 20 standalone MCP server examples you can run level by level.

## Prerequisites

1. Python 3.10+
2. MCP Python SDK installed:

```bash
pip install "mcp[cli]"
```

## How to Run Any Server

From project root:

```bash
python mcp_servers/server_01_hello.py
```

All examples default to `stdio` transport unless noted.

## Level-by-Level Files

Beginner:

1. `server_01_hello.py` - hello + echo
2. `server_02_calculator.py` - arithmetic tools
3. `server_03_text_utils.py` - text helpers
4. `server_04_datetime.py` - time and timezone tools
5. `server_05_json_toolkit.py` - JSON validate/format/merge
6. `server_06_unit_converter.py` - temperature + distance conversion

Intermediate:

7. `server_07_todo_memory.py` - in-memory CRUD tasks
8. `server_08_notes_store.py` - file-backed note store
9. `server_09_file_reader.py` - safe file listing and reading
10. `server_10_csv_inspector.py` - schema and preview from CSV
11. `server_11_sqlite_query.py` - guarded SQLite SELECT queries
12. `server_12_http_fetch.py` - allowlisted HTTP JSON fetch

Advanced:

13. `server_13_async_jobs.py` - async job queue pattern
14. `server_14_ttl_cache.py` - TTL cache for expensive operations
15. `server_15_rate_limit.py` - simple per-client rate limit
16. `server_16_auth_guard.py` - token-protected tool access
17. `server_17_resources.py` - MCP resources
18. `server_18_prompts.py` - MCP prompts
19. `server_19_composed_workflow.py` - business workflow orchestration
20. `server_20_production_template.py` - production template with metrics

## Production Template Transport Options

For `server_20_production_template.py`:

- `MCP_TRANSPORT=stdio` (default)
- `MCP_TRANSPORT=streamable-http`
- `MCP_TRANSPORT=sse`

Optional:

- `MCP_HOST` (default `127.0.0.1`)
- `MCP_PORT` (default `8000`)

## Notes

- Files are designed as learning examples first.
- Some advanced files intentionally keep logic simple so you can extend them.
- `_compat.py` handles import differences between MCP SDK variants.

