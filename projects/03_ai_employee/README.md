# 03 AI Employee

Virtual AI worker service for teams.

## Features
- Accepts team tasks via API
- Executes work (code/content/analysis/research)
- Tracks status in DB
- Supports human approval workflow

## Run
```bash
pip install -r requirements.txt
copy .env.example .env
uvicorn app:app --reload --port 8203
```

## Endpoints
- `POST /api/tasks`
- `POST /api/tasks/{task_id}/approve`
- `GET /api/tasks/{task_id}`
- `GET /api/tasks`

## Notes
- In production, add Slack/Discord notification hooks when task status changes.
