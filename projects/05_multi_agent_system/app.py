from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

from agents import Agent, Runner
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel, Session, create_engine


class Settings(BaseSettings):
    database_url: str = "sqlite:///./multi_agent_system.db"
    openai_api_key: str | None = None
    model_name: str = "gpt-4.1"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
if settings.openai_api_key and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)


class ProjectRunLog(SQLModel, table=True):
    __tablename__ = "project_run_logs"

    id: int | None = SQLField(default=None, primary_key=True)
    project_name: str
    request_json: str
    response_json: str
    status: str
    created_at: datetime = SQLField(default_factory=datetime.utcnow)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class ProjectRunRequest(BaseModel):
    project: str
    deadline: str
    topics: list[str]


class TopicResult(BaseModel):
    topic: str
    research_summary: str
    writing_draft: str
    analysis_notes: str
    quality_score: int


class ProjectRunResponse(BaseModel):
    project: str
    deadline: str
    topic_results: list[TopicResult]
    project_manager_status: str
    next_actions: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ResearchOutput(BaseModel):
    summary: str
    key_points: list[str] = Field(default_factory=list)


class WritingOutput(BaseModel):
    title: str
    draft: str


class AnalysisOutput(BaseModel):
    notes: str
    quality_score: int


class PMOutput(BaseModel):
    status: str
    next_actions: list[str] = Field(default_factory=list)
    manager_notes: str


research_agent = Agent(
    name="Research Agent",
    model=settings.model_name,
    instructions="Gather focused research findings for the topic and deadline.",
    output_type=ResearchOutput,
)
writing_agent = Agent(
    name="Writing Agent",
    model=settings.model_name,
    instructions="Draft clear content from research summary and key points.",
    output_type=WritingOutput,
)
analysis_agent = Agent(
    name="Analysis Agent",
    model=settings.model_name,
    instructions="Evaluate draft quality and return practical improvement notes with score 1-100.",
    output_type=AnalysisOutput,
)
pm_agent = Agent(
    name="Project Manager Agent",
    model=settings.model_name,
    instructions=(
        "Coordinate multi-agent outputs, report status, and provide prioritized next actions "
        "until human approval."
    ),
    output_type=PMOutput,
)


async def run_pipeline(req: ProjectRunRequest) -> tuple[list[TopicResult], PMOutput]:
    topic_results: list[TopicResult] = []

    for topic in req.topics:
        research = await Runner.run(
            research_agent,
            json.dumps({"project": req.project, "topic": topic, "deadline": req.deadline}),
        )
        research_out = research.final_output

        writing = await Runner.run(
            writing_agent,
            json.dumps(
                {
                    "project": req.project,
                    "topic": topic,
                    "research_summary": research_out.summary,
                    "key_points": research_out.key_points,
                }
            ),
        )
        writing_out = writing.final_output

        analysis = await Runner.run(
            analysis_agent,
            json.dumps({"project": req.project, "topic": topic, "draft": writing_out.draft}),
        )
        analysis_out = analysis.final_output

        topic_results.append(
            TopicResult(
                topic=topic,
                research_summary=research_out.summary,
                writing_draft=writing_out.draft,
                analysis_notes=analysis_out.notes,
                quality_score=analysis_out.quality_score,
            )
        )

    pm = await Runner.run(
        pm_agent,
        json.dumps(
            {
                "project": req.project,
                "deadline": req.deadline,
                "topic_results": [x.model_dump() for x in topic_results],
            }
        ),
    )
    return topic_results, pm.final_output


app = FastAPI(title="Multi-Agent System API", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/projects/run", response_model=ProjectRunResponse)
async def run_project(req: ProjectRunRequest, session: Session = Depends(get_session)) -> ProjectRunResponse:
    try:
        topic_results, pm_output = await run_pipeline(req)
        response = ProjectRunResponse(
            project=req.project,
            deadline=req.deadline,
            topic_results=topic_results,
            project_manager_status=pm_output.status,
            next_actions=pm_output.next_actions,
            metadata={"manager_notes": pm_output.manager_notes},
        )
        status = "success"
    except Exception as exc:
        response = ProjectRunResponse(
            project=req.project,
            deadline=req.deadline,
            topic_results=[],
            project_manager_status="failed",
            next_actions=["debug_pipeline", "retry_after_fix"],
            metadata={"error": str(exc)},
        )
        status = "error"

    session.add(
        ProjectRunLog(
            project_name=req.project,
            request_json=json.dumps(req.model_dump(), ensure_ascii=False),
            response_json=json.dumps(response.model_dump(), ensure_ascii=False),
            status=status,
        )
    )
    session.commit()
    return response

