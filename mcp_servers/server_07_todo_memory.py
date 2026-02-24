"""07 Intermediate: In-memory TODO manager."""

from _compat import MCPServer

mcp = MCPServer("server-07-todo-memory")

_tasks: dict[int, dict] = {}
_next_id = 1


@mcp.tool()
def create_task(title: str) -> dict:
    global _next_id
    task = {"id": _next_id, "title": title, "done": False}
    _tasks[_next_id] = task
    _next_id += 1
    return task


@mcp.tool()
def list_tasks() -> list[dict]:
    return sorted(_tasks.values(), key=lambda t: t["id"])


@mcp.tool()
def complete_task(task_id: int) -> dict:
    if task_id not in _tasks:
        raise ValueError(f"Task {task_id} not found.")
    _tasks[task_id]["done"] = True
    return _tasks[task_id]


@mcp.tool()
def delete_task(task_id: int) -> dict:
    if task_id not in _tasks:
        raise ValueError(f"Task {task_id} not found.")
    return _tasks.pop(task_id)


if __name__ == "__main__":
    mcp.run(transport="stdio")

