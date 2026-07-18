# Deployment Notes

This project supports both local Docker Compose development and a deployed
production-style environment. The frontend and backend are deployed as separate
Vercel projects, while PostgreSQL persistence is provided by Neon.

## Deployed Environment

| Component | Deployment |
| :--- | :--- |
| Frontend | `https://ai-job-application-tracker-alpha.vercel.app` |
| Backend | `https://ai-job-application-agent-api.vercel.app` |
| API documentation | `https://ai-job-application-agent-api.vercel.app/docs` |
| Database | Neon PostgreSQL |

The deployed backend uses a pooled Neon connection for application requests and
a direct connection for Alembic migrations.

The public demo currently uses `ANALYSIS_PROVIDER=mock`, so it does not require
an OpenAI API key or incur OpenAI API usage.

## Services

The application has three runtime components:

1. **Frontend**
   - Next.js application
   - Serves the dashboard, application detail pages, forms, and analysis UI

2. **Backend**
   - FastAPI application
   - Exposes application CRUD endpoints
   - Runs analysis provider logic
   - Stores generated analyses

3. **Database**
   - PostgreSQL
   - Stores applications, resume projects, and analysis records

## Required Environment Variables

| Variable | Used by | Secret | Description |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | Backend | Yes | PostgreSQL connection string |
| `API_URL` | Frontend server | No | Server-side URL for calling the backend |
| `NEXT_PUBLIC_API_URL` | Browser | No | Browser-visible backend API URL |
| `ANALYSIS_PROVIDER` | Backend | No | Selects `mock` or `openai` |
| `OPENAI_MODEL` | Backend | No | Model name passed to the OpenAI provider |
| `OPENAI_API_KEY` | Backend | Yes | OpenAI API key, only required for `openai` provider |

## Secret Handling

Do not commit real secrets.

The following values should be stored in the deployment platform's secret
manager or environment variable system:

- `DATABASE_URL`
- `OPENAI_API_KEY`

Never expose secrets through variables prefixed with `NEXT_PUBLIC_`, because
those values are intended for browser-visible frontend configuration.

## Provider Defaults

The safe default provider is:

```env
ANALYSIS_PROVIDER=mock
```

This keeps the application usable without external credentials and makes local
testing deterministic.

To enable the OpenAI-backed provider in a deployed environment:

```env
ANALYSIS_PROVIDER=openai
OPENAI_MODEL=gpt-5.5
OPENAI_API_KEY=your_secret_key
```

If `ANALYSIS_PROVIDER=openai` is selected without an API key, the backend should
return:

```json
{
  "detail": "Analysis provider unavailable"
}
```

with HTTP status `503 Service Unavailable`.

## Local Docker Compose Caveats

The included `docker-compose.yml` is intended for local development.

It uses:

- local container ports
- local bind mounts
- a local PostgreSQL container
- development-oriented service names
- default local credentials

For production, prefer:

- managed PostgreSQL
- platform-managed secrets
- separate frontend and backend deployment targets
- HTTPS public URLs
- no source-code bind mounts
- explicit migration execution during release

## Database Migrations

Before running the backend against a fresh database, apply migrations:

```bash
docker compose exec backend alembic upgrade head
```

For production-style deployment, run the equivalent migration command as part of
the release process before serving traffic.

## Resume Project Seed Data

The application expects stored resume projects for analysis matching.

Seed them with:

```bash
docker compose exec backend python -m app.scripts.seed_resume_projects
```

In a deployed environment, run the equivalent command once after migrations, or
replace it with an admin workflow later.

## Health Checks

Backend health endpoint:

```text
GET /health
```

Database health endpoint:

```text
GET /health/db
```

Use these endpoints to confirm the backend is running and can reach PostgreSQL.

## Frontend and Backend URLs

The frontend uses two API URL concepts:

```env
API_URL=
NEXT_PUBLIC_API_URL=
```

`API_URL` is for server-side frontend requests.

`NEXT_PUBLIC_API_URL` is for browser-side requests and must be reachable from the
user's browser.

Example production-style setup:

```env
API_URL=http://backend.internal:8000
NEXT_PUBLIC_API_URL=https://api.example.com
```

## Deployment Checklist

Before deployment:

- [ ] Set `DATABASE_URL`
- [ ] Run Alembic migrations
- [ ] Seed resume projects
- [ ] Set `ANALYSIS_PROVIDER`
- [ ] Keep `OPENAI_API_KEY` secret
- [ ] Verify `NEXT_PUBLIC_API_URL` is browser-reachable
- [ ] Confirm `/health` returns 200
- [ ] Confirm `/health/db` returns 200
- [ ] Run backend tests
- [ ] Run frontend lint and build checks

## Recommended Verification Commands

```bash
docker compose exec backend pytest
docker compose exec frontend npm run lint
docker compose run --rm frontend npm run build
```

For OpenAI provider verification, follow:

```text
docs/openai-smoke-test.md
```