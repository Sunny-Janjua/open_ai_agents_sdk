# 02 Autonomous Business Agent

Autonomous business operations backend for:
- Lead generation
- Email campaigns
- Social media planning
- Meeting scheduling
- Metrics tracking

## Stack
- FastAPI
- SQLModel + PostgreSQL (SQLite fallback)
- OpenAI Agents SDK
- Optional Playwright + API integrations (SendGrid, LinkedIn, etc.)

## Run
```bash
pip install -r requirements.txt
copy .env.example .env
uvicorn app:app --reload --port 8202
```

## API
`POST /api/business_task`

Example:
```json
{
  "task": "email_campaign",
  "email_list": ["a@b.com", "c@d.com"],
  "subject": "New Product Launch",
  "content": "Check out our new product..."
}
```

## Notes
- Replace tool stubs with real APIs in production.
- Every request and result is logged to `business_action_logs`.
