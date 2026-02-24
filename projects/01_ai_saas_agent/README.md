# 01 AI SaaS Agent

AI SaaS backend with 4 services:
- Generate blogs from titles
- Create resumes from structured inputs
- Summarize articles
- Analyze data

## Stack
- FastAPI
- SQLModel + PostgreSQL (SQLite fallback)
- OpenAI Agents SDK

## Run
```bash
pip install -r requirements.txt
copy .env.example .env
uvicorn app:app --reload --port 8201
```

## API
`POST /api/saas_task`

Example request:
```json
{
  "task": "generate_blog",
  "title": "FastAPI AI Agents SDK Tutorial",
  "keywords": ["FastAPI", "Agents SDK", "AI"]
}
```

Example response:
```json
{
  "status": "success",
  "task": "generate_blog",
  "content": "...",
  "next_actions": ["create_linkedin_post", "generate_thumbnail"],
  "metadata": {}
}
```

## Notes
- Every request/response is logged in table `saas_request_logs`.
- Input is validated by task type before calling the agent.
