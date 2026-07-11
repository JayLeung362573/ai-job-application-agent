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

def test_get_application_by_id(client: TestClient) -> None:
    payload = {
        "company": "Example Systems",
        "title": "Full Stack Intern",
        "location": "Burnaby, BC",
        "job_url": "https://example.com/jobs/full-stack-intern",
        "status": "SAVED",
        "job_description": "Full stack internship using React, TypeScript, APIs, and PostgreSQL.",
        "notes": "Useful for frontend and backend practice.",
    }

    create_response = client.post("/applications", json=payload)

    assert create_response.status_code == 201

    created_application = create_response.json()
    application_id = created_application["id"]

    get_response = client.get(f"/applications/{application_id}")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["id"] == application_id
    assert data["company"] == payload["company"]
    assert data["title"] == payload["title"]
    assert data["status"] == payload["status"]


def test_get_application_by_id_returns_404_for_missing_application(
    client: TestClient,
) -> None:
    response = client.get("/applications/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}

def test_update_application_status_and_notes(client: TestClient) -> None:
    payload = {
        "company": "Example Cloud",
        "title": "Backend Intern",
        "location": "Vancouver, BC",
        "job_url": "https://example.com/jobs/backend-intern",
        "status": "SAVED",
        "job_description": (
            "Backend internship using Python, FastAPI, PostgreSQL, Docker, "
            "and API testing."
        ),
        "notes": "Need to tailor resume.",
    }

    create_response = client.post("/applications", json=payload)
    assert create_response.status_code == 201

    application_id = create_response.json()["id"]

    update_response = client.patch(
        f"/applications/{application_id}",
        json={
            "status": "APPLIED",
            "notes": "Applied with tailored backend resume.",
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == application_id
    assert data["status"] == "APPLIED"
    assert data["notes"] == "Applied with tailored backend resume."

    # Fields not included in the PATCH body should remain unchanged.
    assert data["company"] == payload["company"]
    assert data["title"] == payload["title"]
    assert data["job_description"] == payload["job_description"]


def test_update_application_returns_404_for_missing_application(
    client: TestClient,
) -> None:
    response = client.patch(
        "/applications/00000000-0000-0000-0000-000000000000",
        json={"status": "APPLIED"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}


def test_update_application_rejects_invalid_status(client: TestClient) -> None:
    payload = {
        "company": "Example Invalid Status",
        "title": "Software Intern",
        "location": "Remote",
        "job_url": "https://example.com/jobs/software-intern",
        "status": "SAVED",
        "job_description": "Software internship using APIs and databases.",
        "notes": "Testing invalid status.",
    }

    create_response = client.post("/applications", json=payload)
    assert create_response.status_code == 201

    application_id = create_response.json()["id"]

    response = client.patch(
        f"/applications/{application_id}",
        json={"status": "NOT_A_REAL_STATUS"},
    )

    assert response.status_code == 422

def test_delete_application(client: TestClient) -> None:
    payload = {
        "company": "Example Delete Test",
        "title": "Software Intern",
        "location": "Vancouver, BC",
        "job_url": "https://example.com/jobs/delete-test",
        "status": "SAVED",
        "job_description": "Software internship using APIs and databases.",
        "notes": "This application will be deleted.",
    }

    create_response = client.post("/applications", json=payload)
    assert create_response.status_code == 201

    application_id = create_response.json()["id"]

    delete_response = client.delete(f"/applications/{application_id}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(f"/applications/{application_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Application not found"}


def test_delete_application_returns_404_for_missing_application(
    client: TestClient,
) -> None:
    response = client.delete(
        "/applications/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}

def test_list_applications_filters_by_status(client: TestClient) -> None:
    payload = {
        "company": "Status Filter Systems",
        "title": "Backend Engineering Intern",
        "location": "Vancouver, BC",
        "job_url": "https://example.com/jobs/status-filter",
        "status": "OFFER",
        "job_description": "Backend internship using Python and PostgreSQL.",
        "notes": "Testing application status filtering.",
    }

    create_response = client.post("/applications", json=payload)
    assert create_response.status_code == 201

    created_application = create_response.json()

    response = client.get("/applications?status=OFFER")

    assert response.status_code == 200

    applications = response.json()

    assert len(applications) > 0
    assert all(
        application["status"] == "OFFER"
        for application in applications
    )
    assert any(
        application["id"] == created_application["id"]
        for application in applications
    )

def test_list_applications_searches_case_insensitively(
    client: TestClient,
) -> None:
    payload = {
        "company": "Quantum Search Systems",
        "title": "Platform Engineering Intern",
        "location": "Burnaby, BC",
        "job_url": "https://example.com/jobs/quantum-search",
        "status": "SAVED",
        "job_description": "Platform internship using APIs and containers.",
        "notes": "Testing case-insensitive keyword search.",
    }

    create_response = client.post("/applications", json=payload)
    assert create_response.status_code == 201

    created_application = create_response.json()

    response = client.get("/applications?q=QUANTUM")

    assert response.status_code == 200

    applications = response.json()

    assert any(
        application["id"] == created_application["id"]
        for application in applications
    )

def test_list_applications_combines_search_and_status_filter(
    client: TestClient,
) -> None:
    applied_payload = {
        "company": "Vector Sentinel Applied",
        "title": "Software Engineering Intern",
        "location": "Remote",
        "job_url": "https://example.com/jobs/vector-applied",
        "status": "APPLIED",
        "job_description": "Unique vector-sentinel platform position.",
        "notes": "Should appear in the combined result.",
    }

    rejected_payload = {
        "company": "Vector Sentinel Rejected",
        "title": "Software Engineering Intern",
        "location": "Remote",
        "job_url": "https://example.com/jobs/vector-rejected",
        "status": "REJECTED",
        "job_description": "Unique vector-sentinel platform position.",
        "notes": "Should not appear in the combined result.",
    }

    applied_response = client.post(
        "/applications",
        json=applied_payload,
    )
    rejected_response = client.post(
        "/applications",
        json=rejected_payload,
    )

    assert applied_response.status_code == 201
    assert rejected_response.status_code == 201

    applied_id = applied_response.json()["id"]
    rejected_id = rejected_response.json()["id"]

    response = client.get(
        "/applications?status=APPLIED&q=vector-sentinel"
    )

    assert response.status_code == 200

    application_ids = {
        application["id"]
        for application in response.json()
    }

    assert applied_id in application_ids
    assert rejected_id not in application_ids

def test_list_applications_rejects_invalid_status_filter(
    client: TestClient,
) -> None:
    response = client.get(
        "/applications?status=NOT_A_REAL_STATUS"
    )

    assert response.status_code == 422