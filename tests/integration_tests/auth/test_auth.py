from pprint import pprint
import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("abcdef@mail.ru", "1239871", 200),
        ("k0t@pes.com", "1234", 200),
        ("k0t@pes.com", "1234", 400),
        ("k0t1@pes.com", "1235", 200),
        ("abcde", "1235", 422),
        ("abcde@abc", "1235", 422),
    ],
)
async def test_auth_flow(
    email: str, password: str, status_code: int, ac: AsyncClient
):
    resp_register_user = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert resp_register_user.status_code == status_code
    if status_code != 200:
        return
    # /login
    resp_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert resp_login.status_code == 200
    assert ac.cookies["access_token"]
    assert "access_token" in resp_login.json()

    # /me
    resp_me = await ac.get("/auth/me")
    assert resp_me.status_code == 200
    user = resp_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    resp_logout = await ac.post("/auth/logout")
    assert resp_logout.status_code == 200
    assert "access_token" not in ac.cookies


async def my_test_register_user(ac):
    print("Создание пользователя")
    response = await ac.post(
        "/auth/register",
        json={
            "email": "abcdef@mail.ru",
            "password": "1239871",
            "name": "Test user auth",
        },
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["data"]["email"] == "abcdef@mail.ru"
    assert res["data"]["id"] == 2
    assert "data" in res
    pprint(ac.cookies["access_token"])


async def my_test_login_user_ac(ac: AsyncClient):
    print("Login пользователя")
    response = await ac.post(
        "/auth/login",
        json={
            "email": "abcdef@mail.ru",
            "password": "1239871",
            "name": "Test user auth",
        },
    )
    assert response.status_code == 200
    assert ac.cookies["access_token"]


async def my_test_me(ac: AsyncClient):
    response = await ac.get(
        "/auth/me",
        params={"email": "abcdef@mail.ru", "id": 1, "name": "Test user auth"},
    )
    assert response.status_code == 200
    assert ac.cookies["access_token"]


async def my_test_logout(ac: AsyncClient):
    response = await ac.get("/auth/logout")
    assert response.status_code == 200
    assert not ac.cookies["access_token"]
