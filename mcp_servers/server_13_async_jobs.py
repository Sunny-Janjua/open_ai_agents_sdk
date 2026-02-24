"""13 Advanced: Async background job manager."""

import asyncio
import uuid

from _compat import MCPServer

mcp = MCPServer("server-13-async-jobs")

_jobs: dict[str, dict] = {}


async def _run_job(job_id: str, seconds: int) -> None:
    _jobs[job_id]["status"] = "running"
    await asyncio.sleep(seconds)
    _jobs[job_id]["status"] = "completed"
    _jobs[job_id]["result"] = f"Job waited {seconds} seconds."


@mcp.tool()
async def submit_wait_job(seconds: int) -> dict:
    if seconds < 0 or seconds > 120:
        raise ValueError("Seconds must be between 0 and 120.")
    job_id = str(uuid.uuid4())
    _jobs[job_id] = {"status": "queued", "result": None}
    asyncio.create_task(_run_job(job_id, seconds))
    return {"job_id": job_id, "status": "queued"}


@mcp.tool()
def job_status(job_id: str) -> dict:
    if job_id not in _jobs:
        raise ValueError("Job not found.")
    return {"job_id": job_id, **_jobs[job_id]}


if __name__ == "__main__":
    mcp.run(transport="stdio")

