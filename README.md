# AI Job Application Tracker & Resume Match Agent

A full-stack application for tracking internship applications and analyzing
job descriptions against stored resume projects.

The project combines a Next.js frontend, FastAPI backend, PostgreSQL database,
and a provider-based analysis architecture designed for future OpenAI
integration.

## Current Features

### Job Application Tracking

- Create, view, edit, and delete job applications
- Track application status:
  - `SAVED`
  - `APPLIED`
  - `INTERVIEW`
  - `OFFER`
  - `REJECTED`
- Store job descriptions, locations, posting URLs, and personal notes
- Search applications by:
  - company
  - position
  - location
  - job description
  - notes
- Filter applications by status
- Combine keyword search and status filtering
- Preserve dashboard filters in the URL

### Frontend Experience

- Responsive application dashboard
- Application detail pages
- Create and edit forms
- Two-step deletion confirmation
- Route-level loading skeletons
- Route-level error boundaries
- Retry failed server-side requests
- Separate missing-resource pages from temporary backend failures

### Resume Match Analysis

- Load an application's job description from PostgreSQL
- Compare the role against stored resume projects
- Extract known technical requirements
- Identify matched and missing skills
- Match relevant projects to job requirements
- Generate resume bullet suggestions
- Generate project-focused interview questions
- Calculate a match score from 0 to 100
- Validate structured analysis output with Pydantic
- Persist each generated analysis in PostgreSQL
- Run or re-run analysis from an application detail page
- Display the latest saved analysis in the frontend
- Show match scores, skill gaps, matched projects, resume suggestions, and interview questions

The current implementation uses a deterministic mock provider. It does not
require API credentials or make external AI requests.

---

## Architecture

```text
Next.js Frontend
       |
       | HTTP
       v
FastAPI Application
       |
       +--> Application CRUD
       |
       +--> AnalysisService
                 |
                 +--> AnalysisProvider interface
                 |        |
                 |        +--> MockAnalysisProvider
                 |        +--> OpenAI provider (planned)
                 |
                 +--> PostgreSQL
```

The analysis workflow is separated into three layers:

1. **API layer**  
   Receives requests and converts domain errors into HTTP responses.

2. **Service layer**  
   Loads applications and resume projects, invokes the configured provider,
   and persists validated results.

3. **Provider layer**  
   Generates an `AnalysisResult` without depending on FastAPI, SQLAlchemy, or
   a specific AI vendor.

This design allows the deterministic mock provider to be replaced by an
OpenAI-backed provider without changing the API response schema.

---

## OpenAI Provider

The backend includes an `OpenAIAnalysisProvider` that uses the OpenAI Python SDK
and the Responses API structured-output parsing flow.

The provider is implemented but is not the default runtime provider yet. The
application still uses the deterministic mock provider unless the dependency
configuration is changed in a later step.

This allows the full project to keep working locally and in tests without an
API key.

## Structured Analysis Output

Each analysis contains:

- required skills
- preferred skills
- role responsibilities
- matched resume projects
- missing skills
- tailored resume bullet suggestions
- interview questions
- a match score from 0 to 100

Example response structure:

```json
{
  "required_skills": [
    "Python",
    "FastAPI",
    "React"
  ],
  "preferred_skills": [],
  "responsibilities": [
    "Build and maintain software aligned with the job requirements."
  ],
  "matched_projects": [
    {
      "project_name": "Smart Farm IoT Data Pipeline",
      "matched_skills": [
        "Python",
        "FastAPI"
      ],
      "reason": "The project demonstrates relevant backend experience."
    }
  ],
  "missing_skills": [
    "React"
  ],
  "suggested_bullets": [
    {
      "project_name": "Smart Farm IoT Data Pipeline",
      "bullet": "Built a containerized telemetry pipeline using FastAPI.",
      "target_skill": "FastAPI"
    }
  ],
  "interview_questions": [
    "How did you use FastAPI in Smart Farm IoT Data Pipeline?"
  ],
  "match_score": 67,
  "id": "analysis-uuid",
  "application_id": "application-uuid",
  "created_at": "2026-01-01T00:00:00Z"
}
```

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Backend | Python, FastAPI, Pydantic |
| Database | PostgreSQL, SQLAlchemy, Alembic |
| Testing | Pytest, FastAPI TestClient |
| Infrastructure | Docker, Docker Compose |

---

## Local Development

### Requirements

- Docker
- Docker Compose

### Start the application

```bash
docker compose up --build
```

Services:

| Service | URL |
| :--- | :--- |
| Frontend | `http://localhost:3000` |
| Backend API | `http://localhost:8000` |
| FastAPI documentation | `http://localhost:8000/docs` |
| Backend health check | `http://localhost:8000/health` |

### Apply database migrations

```bash
docker compose exec backend alembic upgrade head
```

### Seed resume projects

```bash
docker compose exec backend python -m app.scripts.seed_resume_projects
```

The seed command inserts or updates:

- Smart Farm IoT Data Pipeline
- Distributed Graph Analytics Engine
- C++ WebSocket Multiplayer Game Server

---

## API Endpoints

### Health

```text
GET /health
GET /health/db
```

### Resume Projects

```text
GET /resume-projects
```

### Applications

```text
POST /applications/{application_id}/analyze
GET  /applications/{application_id}/analysis
GET    /applications/{application_id}
PATCH  /applications/{application_id}
DELETE /applications/{application_id}
```

### Analysis

```text
POST /applications/{application_id}/analyze
```

Each analysis request currently creates a new record in PostgreSQL.

Example:

```bash
curl -X POST \
  http://localhost:8000/applications/{application_id}/analyze
```

Retrieve the most recently created analysis:

```bash
curl \
  http://localhost:8000/applications/{application_id}/analysis
```

The endpoint returns 404 Analysis not found when the application exists but
has not been analyzed.

### Application Query Parameters

`GET /applications` supports:

| Parameter | Description |
| :--- | :--- |
| `q` | Case-insensitive search across application text fields |
| `status` | Filter by application status |

Examples:

```text
GET /applications?q=python
GET /applications?status=APPLIED
GET /applications?q=python&status=APPLIED
```

---

## Frontend Routes

| Route | Description |
| :--- | :--- |
| `/` | Application dashboard |
| `/?q={keyword}&status={status}` | Filtered dashboard |
| `/applications/new` | Create application form |
| `/applications/{id}` | Application detail page |
| `/applications/{id}/edit` | Edit application form |

The application detail page can generate a new analysis and display the latest
saved result, including skill gaps, matched projects, resume suggestions, and
interview questions.

---

## Testing

Apply migrations before running the test suite:

```bash
docker compose exec backend alembic upgrade head
```

Run all backend tests:

```bash
docker compose exec backend pytest
```

The test suite covers:

- application health and database connectivity
- resume project retrieval
- application creation and listing
- application detail retrieval
- partial application updates
- application deletion
- missing-resource handling
- invalid UUID and status validation
- keyword search
- status filtering
- combined search and filtering
- structured analysis schema validation
- analysis score validation
- deterministic mock provider behavior
- skill and project matching
- analysis service persistence
- provider failure handling
- application analysis API responses
- analysis records saved in PostgreSQL
- latest application analysis retrieval
- applications without saved analyses

Run frontend checks:

```bash
docker compose exec frontend npm run lint
docker compose run --rm frontend npm run build
```

---

## Current Limitations

- Analysis currently uses a deterministic mock provider
- OpenAI API integration has not been added
- Re-running analysis creates an additional database record

---

## Planned Development

1. Select the active analysis provider through configuration
2. Add OpenAI API key and model environment variables
3. Add provider failure and timeout handling
4. Improve prompt quality and analysis evaluation
5. Expand automated frontend and end-to-end tests