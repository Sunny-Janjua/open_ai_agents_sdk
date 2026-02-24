from __future__ import annotations

import json
import os
from datetime import datetime
from enum import Enum
from typing import Any, Literal

from agents import Agent, Runner, function_tool
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel, Session, create_engine


class Settings(BaseSettings):
    database_url: str = "sqlite:///./autonomous_business_agent.db"
    openai_api_key: str | None = None
    model_name: str = "gpt-4.1"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
if settings.openai_api_key and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)


class ActionLog(SQLModel, table=True):
    __tablename__ = "business_action_logs"

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


class BusinessTaskType(str, Enum):
    lead_generation = "lead_generation"
    email_campaign = "email_campaign"
    social_post = "social_post"
    schedule_meeting = "schedule_meeting"
    track_metrics = "track_metrics"


class BusinessTaskRequest(BaseModel):
    task: BusinessTaskType
    company_name: str | None = None
    lead_sources: list[str] | None = None
    email_list: list[str] | None = None
    subject: str | None = None
    content: str | None = None
    platform: str | None = None
    metrics: dict[str, Any] | None = None


class BusinessTaskResponse(BaseModel):
    status: str
    task: str
    action_summary: str
    actions_completed: list[str] = Field(default_factory=list)
    next_action: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class BusinessAgentOutput(BaseModel):
    status: Literal["success", "error"] = "success"
    task: str
    action_summary: str
    actions_completed: list[str] = Field(default_factory=list)
    next_action: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


@function_tool
def estimate_email_send_count(email_list: list[str]) -> dict[str, int]:
    return {"emails_sent": len(email_list)}


@function_tool
def estimate_lead_count(lead_sources: list[str]) -> dict[str, int]:
    return {"lead_sources": len(lead_sources), "estimated_leads": max(5, len(lead_sources) * 10)}


business_agent = Agent(
    name="Autonomous Business Agent",
    model=settings.model_name,
    instructions=(
        "You are an autonomous business agent. Responsibilities: lead generation, "
        "email campaigns, social posting, scheduling, and metrics tracking. "
        "Use tools where useful, keep logs in response metadata, and suggest next growth action."
    ),
    tools=[estimate_email_send_count, estimate_lead_count],
    output_type=BusinessAgentOutput,
)


def extract_payload(req: BusinessTaskRequest) -> dict[str, Any]:
    if req.task == BusinessTaskType.lead_generation:
        if not req.company_name:
            raise ValueError("company_name is required for lead_generation")
        return {"company_name": req.company_name, "lead_sources": req.lead_sources or []}

    if req.task == BusinessTaskType.email_campaign:
        if not req.email_list or not req.subject or not req.content:
            raise ValueError("email_list, subject, content are required for email_campaign")
        return {"email_list": req.email_list, "subject": req.subject, "content": req.content}

    if req.task == BusinessTaskType.social_post:
        if not req.platform or not req.content:
            raise ValueError("platform and content are required for social_post")
        return {"platform": req.platform, "content": req.content}

    if req.task == BusinessTaskType.schedule_meeting:
        if not req.content:
            raise ValueError("content is required for schedule_meeting")
        return {"meeting_context": req.content}

    if req.task == BusinessTaskType.track_metrics:
        return {"metrics": req.metrics or {}}

    raise ValueError(f"Unsupported task: {req.task}")


async def run_business_task(task: str, payload: dict[str, Any]) -> BusinessAgentOutput:
    result = await Runner.run(business_agent, json.dumps({"task": task, **payload}))
    return result.final_output


app = FastAPI(title="Autonomous Business Agent API", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/business_task", response_model=BusinessTaskResponse)
async def business_task(req: BusinessTaskRequest, session: Session = Depends(get_session)) -> BusinessTaskResponse:
    try:
        payload = extract_payload(req)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    try:
        output = await run_business_task(req.task.value, payload)
        response = BusinessTaskResponse(
            status=output.status,
            task=output.task,
            action_summary=output.action_summary,
            actions_completed=output.actions_completed,
            next_action=output.next_action,
            metadata=output.metadata,
        )
        status = "success"
    except Exception as exc:
        response = BusinessTaskResponse(
            status="error",
            task=req.task.value,
            action_summary=f"Task failed: {exc}",
            actions_completed=[],
            next_action="manual_review",
            metadata={},
        )
        status = "error"

    session.add(
        ActionLog(
            task=req.task.value,
            request_json=json.dumps(req.model_dump(), ensure_ascii=False),
            response_json=json.dumps(response.model_dump(), ensure_ascii=False),
            status=status,
        )
    )
    session.commit()
    return response

