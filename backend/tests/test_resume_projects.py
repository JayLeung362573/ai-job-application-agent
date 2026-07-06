from fastapi.testclient import TestClient

from app.scripts.seed_resume_projects import seed_resume_projects


def test_list_resume_projects_returns_seeded_projects(client: TestClient) -> None:
    seed_resume_projects()

    response = client.get("/resume-projects")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3

    project_names = {project["name"] for project in data}

    assert project_names == {
        "Smart Farm IoT Data Pipeline",
        "Distributed Graph Analytics Engine",
        "C++ WebSocket Multiplayer Game Server",
    }


def test_resume_projects_response_shape(client: TestClient) -> None:
    seed_resume_projects()

    response = client.get("/resume-projects")

    assert response.status_code == 200

    first_project = response.json()[0]

    assert "id" in first_project
    assert "name" in first_project
    assert "tech_stack" in first_project
    assert "description" in first_project
    assert "resume_bullets" in first_project
    assert "created_at" in first_project
    assert "updated_at" in first_project

    assert isinstance(first_project["tech_stack"], list)
    assert isinstance(first_project["resume_bullets"], list)