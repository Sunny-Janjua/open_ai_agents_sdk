# 5 Detailed Agent Projects

This directory contains 5 separate, runnable project templates:

1. `01_ai_saas_agent`
2. `02_autonomous_business_agent`
3. `03_ai_employee`
4. `04_ai_automation_agency`
5. `05_multi_agent_system`

## Quick Start (Any Project)

```bash
cd projects/<project_folder>
pip install -r requirements.txt
copy .env.example .env
uvicorn app:app --reload --port <port>
```

Recommended ports:
- `01_ai_saas_agent`: `8201`
- `02_autonomous_business_agent`: `8202`
- `03_ai_employee`: `8203`
- `04_ai_automation_agency`: `8204`
- `05_multi_agent_system`: `8205`

## Core Endpoints

- AI SaaS Agent: `POST /api/saas_task`
- Autonomous Business Agent: `POST /api/business_task`
- AI Employee: `POST /api/tasks`, `POST /api/tasks/{id}/approve`
- AI Automation Agency: `POST /api/automation/request`
- Multi-Agent System: `POST /api/projects/run`

## Notes

- Each project includes input validation and structured JSON output.
- Each project logs requests/results in SQLModel tables.
- Set `DATABASE_URL` in `.env` for PostgreSQL, or use SQLite defaults.
