from __future__ import annotations

import json
import os
from datetime import datetime
from enum import Enum
from typing import Literal

from agents import Agent, Runner
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel, Session, create_engine, select


class Settings(BaseSettings):
    database_url: str = "sqlite:///./ai_employee.db"
    openai_api_key: str | None = None
    model_name: str = "gpt-4.1"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
if settings.openai_api_key and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)


class EmployeeTask(SQLModel, table=True):
    __tablename__ = "employee_tasks"

    id: int | None = SQLField(default=None, primary_key=True)
    task_type: str
    description: str
    language: str | None = None
    requires_human_approval: bool = False
    status: str = "created"
    result: str | None = None
    documentation: str | None = None
    next_task_suggestion: str | None = None
    created_at: datetime = SQLField(default_factory=datetime.utcnow)
    updated_at: datetime = SQLField(default_factory=datetime.utcnow)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class EmployeeTaskType(str, Enum):
    write_code = "write_code"
    write_content = "write_content"
    run_analysis = "run_analysis"
    do_research = "do_research"


class EmployeeTaskCreate(BaseModel):
    task: EmployeeTaskType
    description: str
    language: str | None = None
    requires_human_approval: bool = False


class EmployeeTaskRead(BaseModel):
    id: int
    task: str
    status: str
    result: str | None
    documentation: str | None
    next_task_suggestion: str | None


class EmployeeOutput(BaseModel):
    status: Literal["completed", "failed"] = "completed"
    result: str
    documentation: str
    next_task_suggestion: str


employee_agent = Agent(
    name="AI Employee",
    model=settings.model_name,
    instructions=(
        "You are an AI Employee in a company. Receive task input, execute it autonomously, "
        "document your work, and suggest the next task. Notify humans only for approval or errors."
    ),
    output_type=EmployeeOutput,
)


async def run_employee_task(task_type: str, description: str, language: str | None) -> EmployeeOutput:
    payload = {"task": task_type, "description": description, "language": language}
    result = await Runner.run(employee_agent, json.dumps(payload))
    return result.final_output


def to_read(task: EmployeeTask) -> EmployeeTaskRead:
    return EmployeeTaskRead(
        id=task.id or 0,
        task=task.task_type,
        status=task.status,
        result=task.result,
        documentation=task.documentation,
        next_task_suggestion=task.next_task_suggestion,
    )


async def execute_task(task: EmployeeTask, session: Session) -> EmployeeTask:
    task.status = "in_progress"
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    try:
        output = await run_employee_task(task.task_type, task.description, task.language)
        task.status = output.status
        task.result = output.result
        task.documentation = output.documentation
        task.next_task_suggestion = output.next_task_suggestion
    except Exception as exc:
        task.status = "failed"
        task.result = f"Task failed: {exc}"
        task.documentation = "Execution error encountered."
        task.next_task_suggestion = "Manual intervention required."

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


app = FastAPI(title="AI Employee API", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/tasks", response_model=EmployeeTaskRead)
async def create_task(req: EmployeeTaskCreate, session: Session = Depends(get_session)) -> EmployeeTaskRead:
    task = EmployeeTask(
        task_type=req.task.value,
        description=req.description,
        language=req.language,
        requires_human_approval=req.requires_human_approval,
        status="pending_approval" if req.requires_human_approval else "created",
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    if task.requires_human_approval:
        return to_read(task)

    task = await execute_task(task, session)
    return to_read(task)


@app.post("/api/tasks/{task_id}/approve", response_model=EmployeeTaskRead)
async def approve_task(task_id: int, session: Session = Depends(get_session)) -> EmployeeTaskRead:
    task = session.get(EmployeeTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != "pending_approval":
        raise HTTPException(status_code=400, detail="Task is not pending approval")

    task = await execute_task(task, session)
    return to_read(task)


@app.get("/api/tasks/{task_id}", response_model=EmployeeTaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)) -> EmployeeTaskRead:
    task = session.get(EmployeeTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return to_read(task)


@app.get("/api/tasks", response_model=list[EmployeeTaskRead])
def list_tasks(session: Session = Depends(get_session)) -> list[EmployeeTaskRead]:
    rows = session.exec(select(EmployeeTask).order_by(EmployeeTask.id.desc())).all()
    return [to_read(row) for row in rows]

