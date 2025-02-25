# ruff : noqa: E402
# спец файл для того чтобы при каждом прогоне
# тестов выполнялся. Файл настроечный - основной настроечный
from unittest import mock

mock.patch(
    "fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f
).start()

import json
from pprint import pprint

import pytest

from src.api.dependencies import get_db
from src.config import settings
from src.database import (
    BaseModelORM,
    engine_null_pull,
    new_async_session_maker_null_pool,
)
from src.main import app
from src.models import *  # noqa
from httpx import AsyncClient

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


# фикстура, которая вернет подключение в БД
@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(
        session_factory=new_async_session_maker_null_pool
    ) as db:
        yield db


async def get_db_null_pull() -> DBManager:
    async with DBManager(
        session_factory=new_async_session_maker_null_pool
    ) as db:
        pprint("Перезаписан метод работы с БД")
        yield db


# для тестов чтобы не было ошибок-необходимо подменить обращение к БД
# это необходимо для теста, который делает API запрос
# и там достаточно "пустого" подключения. Ниже через метод подменяем на новую функцию
app.dependency_overrides[get_db] = get_db_null_pull


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


# автоматически запустить эту функцию но только для сессии т.е. один раз
# т.к. в самом начале тестов прогоняется именно этот файл - первым
# где удаляются и создаются тестовые таблицы
@pytest.fixture(scope="session", autouse=True)
async def setup_DB_main(check_test_mode):
    print("ФИКСТУРА")
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(BaseModelORM.metadata.drop_all)
        await conn.run_sync(BaseModelORM.metadata.create_all)

    with open("tests/hotel.json", encoding="utf-8") as hotels_test:
        hotels_data = json.load(hotels_test)
    with open("tests/rooms.json", encoding="utf-8") as rooms_test:
        rooms_data = json.load(rooms_test)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels_data]
    rooms = [RoomAdd.model_validate(rooms) for rooms in rooms_data]

    async with DBManager(
        session_factory=new_async_session_maker_null_pool
    ) as db_:
        print("Создание тестовых данных - отелей")
        await db_.hotels.add_bulk(hotels)
        print("Создание тестовых данных - комнат")
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://testuser") as ac:
        yield ac


# т.е запускать при каждом прогоне теста
@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_DB_main):
    print("Создание пользователя")
    await ac.post(
        "/auth/register",
        json={
            "email": "abc@mail.ru",
            "password": "123987",
            "name": "Test user",
        },
    )


@pytest.fixture(scope="session", autouse=True)
async def autheticated_user_ac(ac, register_user):
    print("Login пользователя")
    await ac.post(
        "/auth/login",
        json={
            "email": "abc@mail.ru",
            "password": "123987",
            "name": "Test user",
        },
    )
    assert ac.cookies["access_token"]
    # в куках - есть токен - его и вернуть
    # т.е. он будет теперь доступен и далее в ac
    yield ac
