from __future__ import annotations

import json
import os
from datetime import datetime
from enum import Enum
from typing import Any, Literal

from agents import Agent, Runner
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel, Session, create_engine


class Settings(BaseSettings):
    database_url: str = "sqlite:///./ai_saas_agent.db"
    openai_api_key: str | None = None
    model_name: str = "gpt-4.1"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
if settings.openai_api_key and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)


class RequestLog(SQLModel, table=True):
    __tablename__ = "saas_request_logs"

    id: int | None = SQLField(default=None, primary_key=True)
    task: str
    request_json: str
    response_json: str
    status: str
    created_at: datetime = SQLField(default_factory=datetime.utcnow)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class TaskType(str, Enum):
    generate_blog = "generate_blog"
    create_resume = "create_resume"
    summarize_article = "summarize_article"
    analyze_data = "analyze_data"


class SaaSTaskRequest(BaseModel):
    task: TaskType
    title: str | None = None
    keywords: list[str] | None = None
    resume_data: dict[str, Any] | None = None
    article_text: str | None = None
    data: list[dict[str, Any]] | list[float] | None = None
    question: str | None = None


class SaaSTaskResponse(BaseModel):
    status: str
    task: str
    content: str
    next_actions: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SaaSAgentOutput(BaseModel):
    status: Literal["success", "error"] = "success"
    task: str
    content: str
    next_actions: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


saas_agent = Agent(
    name="AI SaaS Agent",
    model=settings.model_name,
    instructions=(
        "You are an AI SaaS agent that provides services: "
        "generate blogs, create resumes, summarize articles, and analyze data. "
        "Accept structured JSON input, return structured JSON output, and suggest next actions."
    ),
    output_type=SaaSAgentOutput,
)


def extract_payload(req: SaaSTaskRequest) -> dict[str, Any]:
    if req.task == TaskType.generate_blog:
        if not req.title:
            raise ValueError("title is required for generate_blog")
        return {"title": req.title, "keywords": req.keywords or []}

    if req.task == TaskType.create_resume:
        if not req.resume_data:
            raise ValueError("resume_data is required for create_resume")
        return {"resume_data": req.resume_data}

    if req.task == TaskType.summarize_article:
        if not req.article_text:
            raise ValueError("article_text is required for summarize_article")
        return {"article_text": req.article_text}

    if req.task == TaskType.analyze_data:
        if req.data is None or not req.question:
            raise ValueError("data and question are required for analyze_data")
        return {"data": req.data, "question": req.question}

    raise ValueError(f"Unsupported task: {req.task}")


async def run_saas_task(task: str, payload: dict[str, Any]) -> SaaSAgentOutput:
    result = await Runner.run(saas_agent, json.dumps({"task": task, **payload}))
    return result.final_output


app = FastAPI(title="AI SaaS Agent API", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/saas_task", response_model=SaaSTaskResponse)
async def saas_task(req: SaaSTaskRequest, session: Session = Depends(get_session)) -> SaaSTaskResponse:
    try:
        payload = extract_payload(req)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    try:
        output = await run_saas_task(req.task.value, payload)
        response = SaaSTaskResponse(
            status=output.status,
            task=output.task,
            content=output.content,
            next_actions=output.next_actions,
            metadata=output.metadata,
        )
        status = "success"
    except Exception as exc:
        response = SaaSTaskResponse(
            status="error",
            task=req.task.value,
            content=f"Task failed: {exc}",
            next_actions=["retry_request", "validate_input"],
            metadata={},
        )
        status = "error"

    session.add(
        RequestLog(
            task=req.task.value,
            request_json=json.dumps(req.model_dump(), ensure_ascii=False),
            response_json=json.dumps(response.model_dump(), ensure_ascii=False),
            status=status,
        )
    )
    session.commit()
    return response

