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