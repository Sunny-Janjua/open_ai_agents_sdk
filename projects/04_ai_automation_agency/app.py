from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Literal

from agents import Agent, Runner
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel, Session, create_engine


class Settings(BaseSettings):
    database_url: str = "sqlite:///./ai_automation_agency.db"
    openai_api_key: str | None = None
    model_name: str = "gpt-4.1"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
if settings.openai_api_key and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)


class AutomationLog(SQLModel, table=True):
    __tablename__ = "automation_logs"

    id: int | None = SQLField(default=None, primary_key=True)
    client_name: str
    platform: str
    request_json: str
    response_json: str
    status: str
    created_at: datetime = SQLField(default_factory=datetime.utcnow)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class AutomationRequest(BaseModel):
    client_name: str
    automation_request: str
    platform: str
    schedule: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AutomationResponse(BaseModel):
    status: str
    automation_created: bool
    workflow_plan: list[str] = Field(default_factory=list)
    report_summary: str
    next_suggestion: str
    platform: str


class AutomationAgentOutput(BaseModel):
    status: Literal["success", "error"] = "success"
    automation_created: bool = True
    workflow_plan: list[str] = Field(default_factory=list)
    report_summary: str
    next_suggestion: str
    platform: str


automation_agent = Agent(
    name="AI Automation Agency Agent",
    model=settings.model_name,
    instructions=(
        "You are an AI Automation Agency agent. "
        "Plan automations for clients, produce client-friendly reports, optimize workflows, "
        "and suggest new opportunities."
    ),
    output_type=AutomationAgentOutput,
)


async def run_automation(payload: dict[str, Any]) -> AutomationAgentOutput:
    result = await Runner.run(automation_agent, json.dumps(payload))
    return result.final_output


app = FastAPI(title="AI Automation Agency API", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/automation/request", response_model=AutomationResponse)
async def automation_request(
    req: AutomationRequest,
    session: Session = Depends(get_session),
) -> AutomationResponse:
    try:
        output = await run_automation(req.model_dump())
        response = AutomationResponse(
            status=output.status,
            automation_created=output.automation_created,
            workflow_plan=output.workflow_plan,
            report_summary=output.report_summary,
            next_suggestion=output.next_suggestion,
            platform=output.platform,
        )
        status = "success"
    except Exception as exc:
        response = AutomationResponse(
            status="error",
            automation_created=False,
            workflow_plan=[],
            report_summary=f"Automation planning failed: {exc}",
            next_suggestion="manual_planning_required",
            platform=req.platform,
        )
        status = "error"

    session.add(
        AutomationLog(
            client_name=req.client_name,
            platform=req.platform,
            request_json=json.dumps(req.model_dump(), ensure_ascii=False),
            response_json=json.dumps(response.model_dump(), ensure_ascii=False),
            status=status,
        )
    )
    session.commit()
    return response

