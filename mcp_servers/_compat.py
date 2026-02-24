"""Compatibility imports for MCP Python SDK variants."""

from __future__ import annotations

try:
    from mcp.server.mcpserver import Context, MCPServer
except Exception:
    from mcp.server.fastmcp import Context, FastMCP as MCPServer

__all__ = ["MCPServer", "Context"]

