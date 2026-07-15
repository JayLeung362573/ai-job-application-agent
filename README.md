# AI Job Application Tracker & Resume Match Agent

A full-stack application for tracking internship applications, storing job descriptions, and analyzing role fit against resume projects.

## Current Status

### Step 1 Completed
* **Next.js frontend** scaffolded
* **FastAPI backend** scaffolded
* **PostgreSQL service** added through Docker Compose
* `/health` endpoint available
* Local Docker development environment configured

---

## Analysis Provider Architecture

The analysis workflow uses a provider abstraction so that application logic
does not depend directly on a specific AI vendor.

The current deterministic mock provider:

- extracts a known set of technical skills from job descriptions
- matches those skills against stored resume projects
- identifies missing skills
- generates predictable interview questions and bullet suggestions
- runs without API credentials or external network calls

A production OpenAI provider can replace the mock implementation without
changing the validated analysis response schema.

## Structured Analysis Schema

AI-generated job analyses use validated nested schemas containing:

- required and preferred skills
- role responsibilities
- matched resume projects
- missing skills
- tailored resume bullet suggestions
- interview questions
- a match score from 0 to 100

The schema is validated before analysis results are stored in PostgreSQL.

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Next.js, React, TypeScript, Tailwind CSS |
| **Backend** | Python, FastAPI |
| **Database** | PostgreSQL |
| **DevOps** | Docker Compose |

---

## Local Development

To start all services locally, run:

```bash
docker compose up --build
```

Frontend:

```bash
http://localhost:3000
```

Backend health check:
```bash
http://localhost:8000/health
```

FastAPI docs:
```bash
http://localhost:8000/docs
```

## Current API Endpoints

```bash
GET  /health
GET  /health/db
GET  /resume-projects
POST /applications
GET  /applications
GET  /applications/{application_id}
PATCH /applications/{application_id}
DELETE /applications/{application_id}
```
Supported query parameters:

- `q`: case-insensitive search across company, title, location, job description, and notes
- `status`: filter by `SAVED`, `APPLIED`, `INTERVIEW`, `OFFER`, or `REJECTED`

Examples:

```text
GET /applications?q=python
GET /applications?status=APPLIED
GET /applications?status=APPLIED&q=python
```

## Frontend Routes

```text
/                   Application dashboard
/applications/{id}  Application detail page
```

The dashboard provides navigation to a read-only detail page showing the
application metadata, job description, notes, and original job posting URL.

```text
/applications/new   Create application form
```
The create application form submits job information to the FastAPI API and
redirects to the new application's detail page after a successful request.

```text
/applications/{id}/edit  Edit application form
```
The edit form loads the existing application data, sends partial updates to
the FastAPI `PATCH /applications/{application_id}` endpoint, and returns to
the updated detail page after a successful request.

```text
/?q={keyword}&status={status}  Filtered application dashboard
```
Filtered application dashboard

## Frontend Features
- Delete an application through a two-step confirmation flow
- Display API errors without leaving the detail page
- Return to the dashboard after a successful deletion
- Search applications by company, title, location, job description, or notes
- Filter applications by status
- Combine keyword search and status filtering
- Preserve filters in the URL for refreshable and shareable dashboard views
- Display route-level error boundaries for dashboard and application pages
- Retry failed server-side data requests without a full browser refresh
- Keep missing applications separate from temporary backend failures

The application detail page includes a danger zone with an explicit
confirmation step before permanently deleting a stored application.

## Seed Data

Seed the resume projects table:

```bash
docker compose exec backend python -m app.scripts.seed_resume_projects
```

The seed script inserts or updates three resume projects:

- Smart Farm IoT Data Pipeline
- Distributed Graph Analytics Engine
- C++ WebSocket Multiplayer Game Server

## Backend Tests

Apply migrations first:

```bash
docker compose exec backend alembic upgrade head
```

Run backend tests:

```bash
docker compose exec backend pytest
```

The current backend test suite covers:

- `GET /health`
- `GET /health/db`
- `GET /resume-projects`
- `POST /applications`
- `GET /applications`
- `GET /applications/{application_id}`
- missing application 404 handling
- `PATCH /applications/{application_id}`
- partial update behavior
- invalid application status validation
- `DELETE /applications/{application_id}`
- delete confirmation through follow-up 404
- application keyword search
- application status filtering
- combined search and status filtering
- invalid status query validation
