import pytest

from app.services.analysis import (
    MockAnalysisProvider,
    ResumeProjectContext,
)


PROJECTS = [
    ResumeProjectContext(
        name="Smart Farm IoT Data Pipeline",
        tech_stack=(
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
            "GitHub Actions",
        ),
        description=(
            "A containerized IoT telemetry pipeline with FastAPI "
            "and PostgreSQL."
        ),
        resume_bullets=(
            (
                "Built a Dockerized IoT telemetry pipeline using "
                "FastAPI and PostgreSQL."
            ),
        ),
    ),
    ResumeProjectContext(
        name="C++ WebSocket Multiplayer Game Server",
        tech_stack=(
            "C++23",
            "WebSockets",
            "GoogleTest",
            "Docker",
        ),
        description=(
            "An event-loop-based multiplayer game server."
        ),
        resume_bullets=(
            (
                "Built an event-loop-based C++23 WebSocket "
                "game server."
            ),
        ),
    ),
]


def test_mock_provider_returns_deterministic_result() -> None:
    provider = MockAnalysisProvider()

    job_description = (
        "We are looking for an intern with Python, FastAPI, "
        "PostgreSQL, Docker, React, and TypeScript experience."
    )

    first_result = provider.analyze(
        job_description=job_description,
        resume_projects=PROJECTS,
    )
    second_result = provider.analyze(
        job_description=job_description,
        resume_projects=PROJECTS,
    )

    assert first_result == second_result


def test_mock_provider_matches_projects_and_missing_skills() -> None:
    provider = MockAnalysisProvider()

    result = provider.analyze(
        job_description=(
            "The role requires Python, FastAPI, PostgreSQL, Docker, "
            "React, and TypeScript."
        ),
        resume_projects=PROJECTS,
    )

    assert result.required_skills == [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "Docker",
        "TypeScript",
        "React",
    ]

    assert result.missing_skills == [
        "TypeScript",
        "React",
    ]

    assert result.match_score == 67

    assert len(result.matched_projects) == 2

    matched_project_names = {
        project.project_name
        for project in result.matched_projects
    }

    assert matched_project_names == {
        "Smart Farm IoT Data Pipeline",
        "C++ WebSocket Multiplayer Game Server",
    }


def test_mock_provider_matches_cplusplus_variants() -> None:
    provider = MockAnalysisProvider()

    result = provider.analyze(
        job_description=(
            "The candidate should have C++ and WebSockets experience."
        ),
        resume_projects=PROJECTS,
    )

    assert result.required_skills == [
        "C++",
        "WebSockets",
    ]
    assert result.missing_skills == []
    assert result.match_score == 100


def test_mock_provider_rejects_empty_job_description() -> None:
    provider = MockAnalysisProvider()

    with pytest.raises(
        ValueError,
        match="Job description cannot be empty",
    ):
        provider.analyze(
            job_description="   ",
            resume_projects=PROJECTS,
        )