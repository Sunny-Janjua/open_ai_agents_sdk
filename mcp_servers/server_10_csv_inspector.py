"""10 Intermediate: CSV inspection tools."""

import csv
from pathlib import Path

from _compat import MCPServer

mcp = MCPServer("server-10-csv-inspector")

ROOT = Path(__file__).resolve().parent


def _safe_csv(path: str) -> Path:
    p = (ROOT / path).resolve()
    if not str(p).startswith(str(ROOT)):
        raise ValueError("Path escapes allowed root.")
    if p.suffix.lower() != ".csv":
        raise ValueError("Only .csv files are allowed.")
    return p


@mcp.tool()
def csv_preview(path: str, rows: int = 5) -> list[dict]:
    csv_path = _safe_csv(path)
    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        output = []
        for idx, row in enumerate(reader):
            if idx >= rows:
                break
            output.append(row)
    return output


@mcp.tool()
def csv_schema(path: str) -> dict:
    csv_path = _safe_csv(path)
    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return {"columns": reader.fieldnames or []}


if __name__ == "__main__":
    mcp.run(transport="stdio")

