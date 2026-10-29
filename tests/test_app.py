import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_create_task_requires_title(client):
    response = client.post("/tasks", json={"description": "no title here"})
    assert response.status_code == 400


def test_create_and_get_task(client):
    create_response = client.post(
        "/tasks", json={"title": "Test Task", "description": "pytest created this"}
    )
    assert create_response.status_code == 201
    new_task = create_response.get_json()
    assert new_task["title"] == "Test Task"

    task_id = new_task["id"]
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["title"] == "Test Task"


def test_get_nonexistent_task(client):
    response = client.get("/tasks/999999")
    assert response.status_code == 404


def test_update_task(client):
    create_response = client.post("/tasks", json={"title": "Original"})
    task_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated", "status": "done"},
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["status"] == "done"


def test_delete_task(client):
    create_response = client.post("/tasks", json={"title": "To be deleted"})
    task_id = create_response.get_json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
