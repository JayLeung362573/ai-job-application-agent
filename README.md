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
GET /health
```

## Next Step

Step 2 will add the PostgreSQL schema for applications, analyses, and resume projects.

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

- ET /health
- GET /health/db
- GET /resume-projects