import uuid

from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.models.analysis import Analysis
from app.scripts.seed_resume_projects import (
    seed_resume_projects,
)


def test_analyze_application_creates_saved_analysis(
    client: TestClient,
) -> None:
    seed_resume_projects()

    application_payload = {
        "company": "Analysis API Test",
        "title": "Software Engineering Intern",
        "location": "Vancouver, BC",
        "job_url": "https://example.com/jobs/analysis-api-test",
        "status": "SAVED",
        "job_description": (
            "We are looking for an intern with Python, FastAPI, "
            "and React experience."
        ),
        "notes": "Testing the analysis endpoint.",
    }

    create_response = client.post(
        "/applications",
        json=application_payload,
    )

    assert create_response.status_code == 201

    application_id = create_response.json()["id"]

    analysis_response = client.post(
        f"/applications/{application_id}/analyze"
    )

    assert analysis_response.status_code == 201

    data = analysis_response.json()

    assert data["application_id"] == application_id

    assert data["required_skills"] == [
        "Python",
        "FastAPI",
        "React",
    ]
    assert data["missing_skills"] == ["React"]
    assert data["match_score"] == 67

    assert len(data["matched_projects"]) >= 1

    matched_project_names = {
        project["project_name"]
        for project in data["matched_projects"]
    }

    assert "Smart Farm IoT Data Pipeline" in matched_project_names

    assert len(data["suggested_bullets"]) >= 1
    assert len(data["interview_questions"]) >= 1

    assert "id" in data
    assert "created_at" in data

    analysis_id = uuid.UUID(data["id"])

    with SessionLocal() as db:
        saved_analysis = db.get(
            Analysis,
            analysis_id,
        )

        assert saved_analysis is not None
        assert str(saved_analysis.application_id) == application_id
        assert saved_analysis.match_score == 67
        assert saved_analysis.missing_skills == ["React"]


def test_analyze_application_returns_404_when_missing(
    client: TestClient,
) -> None:
    response = client.post(
        (
            "/applications/"
            "00000000-0000-0000-0000-000000000000/"
            "analyze"
        )
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found",
    }


def test_analyze_application_rejects_invalid_uuid(
    client: TestClient,
) -> None:
    response = client.post(
        "/applications/not-a-valid-uuid/analyze"
    )

    assert response.status_code == 422

def create_application_for_analysis(
    client: TestClient,
    *,
    company: str,
    job_description: str,
) -> str:
    response = client.post(
        "/applications",
        json={
            "company": company,
            "title": "Software Engineering Intern",
            "location": "Vancouver, BC",
            "job_url": "https://example.com/jobs/latest-analysis",
            "status": "SAVED",
            "job_description": job_description,
            "notes": "Latest analysis endpoint test.",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]

def test_get_latest_application_analysis(
    client: TestClient,
) -> None:
    seed_resume_projects()

    application_id = create_application_for_analysis(
        client,
        company="Latest Analysis API Test",
        job_description=(
            "We need Python and FastAPI experience."
        ),
    )

    first_response = client.post(
        f"/applications/{application_id}/analyze"
    )

    assert first_response.status_code == 201

    update_response = client.patch(
        f"/applications/{application_id}",
        json={
            "job_description": (
                "We need Python, FastAPI, and React experience."
            ),
        },
    )

    assert update_response.status_code == 200

    second_response = client.post(
        f"/applications/{application_id}/analyze"
    )

    assert second_response.status_code == 201

    latest_response = client.get(
        f"/applications/{application_id}/analysis"
    )

    assert latest_response.status_code == 200

    latest_data = latest_response.json()

    assert latest_data["id"] == second_response.json()["id"]
    assert latest_data["id"] != first_response.json()["id"]

    assert latest_data["required_skills"] == [
        "Python",
        "FastAPI",
        "React",
    ]
    assert latest_data["missing_skills"] == ["React"]
    assert latest_data["application_id"] == application_id


def test_get_latest_analysis_returns_404_when_none_exists(
    client: TestClient,
) -> None:
    application_id = create_application_for_analysis(
        client,
        company="No Analysis API Test",
        job_description="We need Python experience.",
    )

    response = client.get(
        f"/applications/{application_id}/analysis"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Analysis not found",
    }


def test_get_latest_analysis_returns_404_for_missing_application(
    client: TestClient,
) -> None:
    response = client.get(
        (
            "/applications/"
            "00000000-0000-0000-0000-000000000000/"
            "analysis"
        )
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found",
    }