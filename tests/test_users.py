import pytest
from httpx import AsyncClient

from .conftest import auth_header


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/users",
        json={
            "username": "Bobby",
            "email": "bobbythebob@example.com",
            "password": "secret_password",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "Bobby"
    assert data["email"] == "bobbythebob@example.com"
    assert "password" not in data
    assert "id" in data


@pytest.mark.asyncio
async def test_login_user_correct(client: AsyncClient):
    await client.post(
        "/users",
        json={
            "username": "Ed",
            "email": "edmail@example.com",
            "password": "secret_password",
        },
    )

    response = await client.post(
        "/users/token",
        data={"username": "Ed", "password": "secret_password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient):
    await client.post(
        "/users",
        json={
            "username": "Cooper",
            "email": "agentcooper@example.com",
            "password": "good_cup_of_coffee",
        },
    )
    login_response = await client.post(
        "users/token", data={"username": "Cooper", "password": "good_cup_of_coffee"}
    )
    token = login_response.json()["access_token"]
    headers = auth_header(token)
    response = await client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "Cooper"
    assert data["email"] == "agentcooper@example.com"


@pytest.mark.asyncio
async def test_register_user_existing(client: AsyncClient):
    await client.post(
        "/users",
        json={
            "username": "Norma",
            "email": "norma123@example.com",
            "password": "12345678910",
        },
    )

    response = await client.post(
        "/users",
        json={
            "username": "Norma",
            "email": "norma123@example.com",
            "password": "12345678910",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


@pytest.mark.asyncio
async def test_login_user_wrong(client: AsyncClient):
    await client.post(
        "/users",
        json={
            "username": "Josie",
            "email": "josieee@example.com",
            "password": "correct_password",
        },
    )
    response = await client.post(
        "/users/token", data={"username": "Josie", "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_get_current_user_unauth(client: AsyncClient):
    response = await client.get("/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
