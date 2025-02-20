from pprint import pprint


async def test_register_user(ac):
    print("Создание пользователя")
    response = await ac.post(
        "/auth/register",
        json={
            "email": "abcdef@mail.ru",
            "password": "1239871",
            "name": "Test user auth"
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["data"]["email"] == "abcdef@mail.ru"
    assert res["data"]["id"] == 2
    assert "data" in res
    pprint(ac.cookies["access_token"])


async def test_login_user_ac(ac):
    print("Login пользователя")
    response = await ac.post(
        "/auth/login",
        json={
            "email": "abcdef@mail.ru",
            "password": "1239871",
            "name": "Test user auth"
        }
    )
    assert response.status_code == 200
    assert ac.cookies["access_token"]


async def test_me(ac, db):
    response = await ac.get(
        "/auth/me",
        params={
            "email": "abcdef@mail.ru",
            "id": 1,
            "name": "Test user auth"
        }
    )
    assert response.status_code == 200
    assert ac.cookies["access_token"]


async def test_logout(ac):
    response = await ac.get(
        "/auth/logout"
    )
    assert response.status_code == 200
    assert not ac.cookies["access_token"]
