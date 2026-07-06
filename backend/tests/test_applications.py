from fastapi.testclient import TestClient


def test_create_application(client: TestClient) -> None:
    payload = {
        "company": "Example Robotics",
        "title": "Software Engineering Intern",
        "location": "Vancouver, BC",
        "job_url": "https://example.com/jobs/software-intern",
        "status": "SAVED",
        "job_description": (
            "We are looking for a software engineering intern with Python, "
            "TypeScript, APIs, PostgreSQL, Docker, and testing experience."
        ),
        "notes": "Good match for backend and full-stack roles.",
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == payload["company"]
    assert data["title"] == payload["title"]
    assert data["location"] == payload["location"]
    assert data["job_url"] == payload["job_url"]
    assert data["status"] == payload["status"]
    assert data["job_description"] == payload["job_description"]
    assert data["notes"] == payload["notes"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_list_applications_includes_created_application(client: TestClient) -> None:
    payload = {
        "company": "Example AI",
        "title": "Backend Engineering Intern",
        "location": "Remote",
        "job_url": "https://example.com/jobs/backend-intern",
        "status": "APPLIED",
        "job_description": "Backend internship using Python, FastAPI, PostgreSQL, and Docker.",
        "notes": "Applied after tailoring resume.",
    }

    create_response = client.post("/applications", json=payload)

    assert create_response.status_code == 201

    list_response = client.get("/applications")

    assert list_response.status_code == 200

    applications = list_response.json()

    assert any(
        application["company"] == payload["company"]
        and application["title"] == payload["title"]
        for application in applications
    )