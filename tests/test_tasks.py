import pytest
from httpx import AsyncClient

from .conftest import auth_header, create_test_user, login_test_user


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    await create_test_user(client)
    token = await login_test_user(client)
    headers = auth_header(token)
    payload = {
        "title": "Write some tests",
        "description": "Tests must be for FastAPI",
        "priority": "S",
    }
    response = await client.post("/tasks", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write some tests"
    assert data["is_done"] is False
    assert data["priority"] == "S"
    assert data["user_id"] is not None
    assert "id" in data


@pytest.mark.asyncio
async def test_get_user_tasks(client: AsyncClient):
    await create_test_user(client)
    token = await login_test_user(client)
    headers = auth_header(token)

    for i in range(1, 5 + 1):
        await client.post("/tasks", json={"title": f"Task {i}"}, headers=headers)

    response = await client.get("/tasks", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    titles = [t["title"] for t in data]
    assert "Task 1" in titles
    assert "Task 2" in titles
    assert "Task 3" in titles
    assert "Task 4" in titles
    assert "Task 5" in titles


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):
    await create_test_user(client)
    token = await login_test_user(client)
    headers = auth_header(token)

    create_response = await client.post(
        "/tasks", json={"title": "Old title"}, headers=headers
    )
    task_id = create_response.json()["id"]

    update_payload = {"title": "New title", "priority": "S"}
    response = await client.patch(
        f"/tasks/{task_id}", json=update_payload, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["priority"] == "S"
    assert data["is_done"] is False


@pytest.mark.asyncio
async def test_get_user_single_task(client: AsyncClient):
    await create_test_user(client)
    token = await login_test_user(client)
    headers = auth_header(token)

    create_response = await client.post(
        "/tasks", json={"title": "Main Goal"}, headers=headers
    )
    task_id = create_response.json()["id"]

    response = await client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Main Goal"


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    await create_test_user(client)
    token = await login_test_user(client)
    headers = auth_header(token)

    create_response = await client.post(
        "/tasks", json={"title": "Will be deleted"}, headers=headers
    )
    task_id = create_response.json()["id"]

    response = await client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 204

    get_response = await client.get(f"/tasks/{task_id}", headers=headers)
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_tasks_using_filters(client: AsyncClient):
    await create_test_user(client)
    token = await login_test_user(client)
    headers = auth_header(token)

    await client.post(
        "/tasks",
        json={"title": "Task 1", "priority": "D"},
        headers=headers,
    )
    task_2 = await client.post(
        "/tasks", json={"title": "Task 2", "priority": "B"}, headers=headers
    )
    task2_id = task_2.json()["id"]
    await client.post(
        "/tasks",
        json={"title": "Task 3", "priority": "S"},
        headers=headers,
    )
    await client.post(
        "/tasks",
        json={"title": "Task 4", "priority": "B"},
        headers=headers,
    )
    await client.post(
        "/tasks", json={"title": "Task 5", "priority": "B"}, headers=headers
    )

    await client.patch(f"/tasks/{task2_id}", json={"is_done": True}, headers=headers)

    response = await client.get("/tasks?priority=B", headers=headers)
    data = response.json()
    assert len(data) == 3
    assert all(t["priority"] == "B" for t in data)

    response = await client.get("/tasks?priority=B", headers=headers)
    data = response.json()
    assert len(data) == 3
    assert data[0]["title"] == "Task 2"
    assert data[1]["title"] == "Task 4"
    assert data[2]["title"] == "Task 5"

    response = await client.get("/tasks?priority=B&is_done=true", headers=headers)
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Task 2"
    assert data[0]["is_done"] is True


@pytest.mark.asyncio
async def test_create_task_without_token(client: AsyncClient):
    response = await client.post("/tasks", json={"title": "Unauthorized task"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_non_existent_task(client: AsyncClient):
    await create_test_user(client)
    token = await login_test_user(client)
    headers = auth_header(token)

    response = await client.get("/tasks/1234", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


@pytest.mark.asyncio
async def test_update_task_as_done(client: AsyncClient):
    await create_test_user(client)
    token = await login_test_user(client)
    headers = auth_header(token)

    create_response = await client.post(
        "/tasks", json={"title": "Task is completed"}, headers=headers
    )
    task_id = create_response.json()["id"]

    response = await client.patch(
        f"/tasks/{task_id}", json={"is_done": True}, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_done"] is True
    assert data["done_time"] is not None
