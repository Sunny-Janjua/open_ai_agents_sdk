# 05 Multi-Agent System

Project orchestration backend with 4 coordinated agents:
- Research Agent
- Writing Agent
- Analysis Agent
- Project Manager Agent

## Flow
1. Research per topic
2. Draft generation
3. Quality analysis
4. PM coordination and next-action planning

## Run
```bash
pip install -r requirements.txt
copy .env.example .env
uvicorn app:app --reload --port 8205
```

## API
`POST /api/projects/run`

Example:
```json
{
  "project": "AI Blog Series",
  "deadline": "2026-03-01",
  "topics": ["FastAPI", "AI Agents"]
}
```

## Notes
- Add Redis/RabbitMQ later if you want distributed message passing.
