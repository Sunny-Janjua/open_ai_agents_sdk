"""09 Intermediate: Safe file reader tools."""

from pathlib import Path

from _compat import MCPServer

mcp = MCPServer("server-09-file-reader")

ROOT = Path(__file__).resolve().parent


def _safe_path(relative_path: str) -> Path:
    target = (ROOT / relative_path).resolve()
    if not str(target).startswith(str(ROOT)):
        raise ValueError("Path escapes allowed root.")
    return target


@mcp.tool()
def list_files(relative_dir: str = ".") -> list[str]:
    directory = _safe_path(relative_dir)
    if not directory.is_dir():
        raise ValueError("Not a directory.")
    return sorted([p.name for p in directory.iterdir()])


@mcp.tool()
def read_text_file(relative_path: str, max_chars: int = 3000) -> str:
    file_path = _safe_path(relative_path)
    if not file_path.exists() or not file_path.is_file():
        raise ValueError("File not found.")
    return file_path.read_text(encoding="utf-8")[:max_chars]


if __name__ == "__main__":
    mcp.run(transport="stdio")

