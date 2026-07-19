# Manual OpenAI Smoke Test

This guide explains how to manually verify the OpenAI-backed analysis provider.

The application uses the deterministic mock provider by default. The OpenAI
provider should only be enabled locally when you intentionally want to test a
real API request.

## Safety Rules

- Do not commit a real `OPENAI_API_KEY`.
- Do not put API keys in frontend code.
- Do not expose API keys through `NEXT_PUBLIC_*` variables.
- Keep the default provider as `mock` for normal local development.
- Use a small test application first before running multiple analyses.

## 1. Confirm the default mock provider works

Start the app with the default configuration:

```bash
docker compose down
docker compose up --build -d
```

Confirm the backend is running:

```bash
docker compose ps
```

Run the backend tests:

```bash
docker compose exec backend pytest
```

The app should work without any OpenAI API key because the default provider is
`mock`.

## 2. Create a local `.env` file

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` locally:

```env
ANALYSIS_PROVIDER=openai
OPENAI_MODEL=gpt-5.6-luna
OPENAI_API_KEY=replace_with_your_real_key
```

The `.env` file is local-only and must not be committed.

## 3. Restart Docker Compose

```bash
docker compose down
docker compose up --build -d
```

Confirm the backend selected the OpenAI provider:

```bash
docker compose exec -T backend python - <<'PY'
from app.api.dependencies import get_analysis_service
from app.services.analysis import OpenAIAnalysisProvider

service = get_analysis_service()

print(type(service.provider).__name__)
print(isinstance(service.provider, OpenAIAnalysisProvider))
print(service.provider.model)
PY
```

Expected output:

```text
OpenAIAnalysisProvider
True
gpt-5.6-luna
```

## 4. Create or find an application

Create a small test application:

```bash
curl -X POST \
  http://localhost:8000/applications \
  -H "Content-Type: application/json" \
  -d '{
    "company": "OpenAI Smoke Test Company",
    "title": "Software Engineering Intern",
    "location": "Vancouver, BC",
    "job_url": "https://example.com/jobs/openai-smoke-test",
    "status": "SAVED",
    "job_description": "We are looking for a software engineering intern with Python, FastAPI, PostgreSQL, Docker, React, and TypeScript experience.",
    "notes": "Manual OpenAI smoke test."
  }' | python3 -m json.tool
```

Copy the returned `id`.

## 5. Run a real analysis request

```bash
curl -i -X POST \
  http://localhost:8000/applications/PASTE_APPLICATION_ID_HERE/analyze
```

Expected result:

```text
HTTP/1.1 201 Created
```

The JSON body should include fields such as:

```json
{
  "required_skills": [],
  "matched_projects": [],
  "missing_skills": [],
  "suggested_bullets": [],
  "interview_questions": [],
  "match_score": 0,
  "id": "...",
  "application_id": "...",
  "created_at": "..."
}
```

The exact analysis content may vary because this request uses a real model.

## 6. Retrieve the saved analysis

```bash
curl \
  http://localhost:8000/applications/PASTE_APPLICATION_ID_HERE/analysis \
  | python3 -m json.tool
```

The returned `id` should match the most recent analysis record.

## 7. Confirm frontend behavior

Open:

```text
http://localhost:3000/applications/PASTE_APPLICATION_ID_HERE
```

The detail page should display the latest analysis result.

Clicking `Run again` should create a new analysis record and refresh the page
with the newest result.

## 8. Common failure cases

### Missing API key

If `ANALYSIS_PROVIDER=openai` but `OPENAI_API_KEY` is empty, the API should
return:

```text
HTTP/1.1 503 Service Unavailable
```

```json
{
  "detail": "Analysis provider unavailable"
}
```

### Invalid key, model access issue, or provider failure

The API should also return:

```text
HTTP/1.1 503 Service Unavailable
```

```json
{
  "detail": "Analysis provider unavailable"
}
```

Check backend logs for details:

```bash
docker compose logs backend
```

## Evaluate the generated analysis

After creating a real OpenAI-backed analysis, run the evaluation script:

```bash
docker compose exec backend python -m app.scripts.evaluate_latest_analysis PASTE_APPLICATION_ID_HERE
```

A clean result looks like:

```text
Analysis evaluation: PASSED
Issues: 0
Warnings: 0
```

A failed result means the analysis was saved successfully, but the generated
content may need review. For example, the evaluator can detect invented project
names, unsupported matched skills, or skills incorrectly marked as missing.

Warnings do not fail the analysis, but they identify weaker output such as very
short suggested bullets.

## 9. Return to the default mock provider

After the smoke test, edit `.env`:

```env
ANALYSIS_PROVIDER=mock
OPENAI_MODEL=gpt-5.6-luna
OPENAI_API_KEY=
```

Restart:

```bash
docker compose down
docker compose up --build -d
```

Confirm the selected provider:

```bash
docker compose exec -T backend python - <<'PY'
from app.api.dependencies import get_analysis_service
from app.services.analysis import MockAnalysisProvider

service = get_analysis_service()

print(type(service.provider).__name__)
print(isinstance(service.provider, MockAnalysisProvider))
PY
```

Expected output:

```text
MockAnalysisProvider
True
```

## Final Checklist

Before committing anything after a smoke test, run:

```bash
git status --short
```

Make sure `.env` is not staged.

Then run:

```bash
docker compose exec backend pytest
docker compose exec frontend npm run lint
docker compose run --rm frontend npm run build
```