# 04 AI Automation Agency

Automation service backend for client workflows.

## Features
- Accept client automation requests
- Produce workflow plans
- Generate reports and optimization suggestions
- Save logs for monitoring and billing

## Run
```bash
pip install -r requirements.txt
copy .env.example .env
uvicorn app:app --reload --port 8204
```

## API
`POST /api/automation/request`

Example:
```json
{
  "client_name": "ABC Corp",
  "automation_request": "Post product updates on Instagram every day at 10am",
  "platform": "Instagram"
}
```

## Notes
- Start with API-first automations, then add Playwright/Selenium where APIs do not exist.
