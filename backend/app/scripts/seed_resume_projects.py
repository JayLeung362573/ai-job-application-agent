from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.resume_project import ResumeProject


SEED_PROJECTS = [
    {
        "name": "Smart Farm IoT Data Pipeline",
        "tech_stack": [
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
            "GitHub Actions",
        ],
        "description": (
            "A containerized IoT telemetry pipeline that simulates concurrent "
            "sensor streams, ingests time-series readings into PostgreSQL, and "
            "exposes FastAPI endpoints for latest readings and field analytics."
        ),
        "resume_bullets": [
            (
                "Built a Dockerized IoT telemetry pipeline simulating 500 concurrent "
                "sensor streams with multithreaded workers batching time-series "
                "readings into PostgreSQL."
            ),
            (
                "Designed partitioned telemetry tables with BRIN indexes and "
                "materialized views, exposing FastAPI endpoints for latest readings "
                "and pre-aggregated field analytics."
            ),
            (
                "Sustained 508.94 committed rows/s with 100% commit success and "
                "zero failed, skipped, or dropped readings; added unit and PostgreSQL "
                "integration tests to GitHub Actions."
            ),
        ],
    },
    {
        "name": "Distributed Graph Analytics Engine",
        "tech_stack": [
            "C++",
            "Python",
            "MPI",
            "Docker",
            "GitHub Actions",
        ],
        "description": (
            "A distributed-memory graph analytics engine for parallel PageRank and "
            "Triangle Counting over CSR/CSC graph representations with configurable "
            "partitioning and communication strategies."
        ),
        "resume_bullets": [
            (
                "Built a distributed-memory MPI graph analytics engine for parallel "
                "PageRank and Triangle Counting over CSR/CSC graph representations."
            ),
            (
                "Implemented an edge-aware partitioner that reduced per-rank edge "
                "workload imbalance from 20.6x to 1.0x on a degree-skewed graph "
                "with 118K edges."
            ),
            (
                "Benchmarked workloads up to 100K vertices and 1M edges across "
                "1--4 MPI processes, achieving up to 3.89x Triangle Counting speedup."
            ),
        ],
    },
    {
        "name": "C++ WebSocket Multiplayer Game Server",
        "tech_stack": [
            "C++23",
            "WebSockets",
            "GoogleTest",
            "Docker",
        ],
        "description": (
            "An event-loop-based C++23 WebSocket multiplayer game server with typed "
            "protocol messages, server-authoritative lobby/session flows, and "
            "defensive networking safeguards."
        ),
        "resume_bullets": [
            (
                "Built an event-loop-based C++23 WebSocket game server that parses "
                "raw payloads into typed std::variant protocol messages through a "
                "transport-agnostic networking layer."
            ),
            (
                "Implemented server-authoritative lobby/session flows with "
                "payload-size limits, input-buffer caps, malformed-message filtering, "
                "GoogleTest protocol tests, and client simulation."
            ),
        ],
    },
]


def seed_resume_projects() -> None:
    inserted_count = 0
    updated_count = 0

    with SessionLocal() as db:
        for project_data in SEED_PROJECTS:
            existing_project = db.scalar(
                select(ResumeProject).where(
                    ResumeProject.name == project_data["name"]
                )
            )

            if existing_project is None:
                db.add(ResumeProject(**project_data))
                inserted_count += 1
            else:
                existing_project.tech_stack = project_data["tech_stack"]
                existing_project.description = project_data["description"]
                existing_project.resume_bullets = project_data["resume_bullets"]
                updated_count += 1

        db.commit()

    print(
        f"Seeded resume projects: "
        f"{inserted_count} inserted, {updated_count} updated."
    )


if __name__ == "__main__":
    seed_resume_projects()