#спец файл для того чтобы при каждом прогоне
#тестов выполнялся. Файл настроечный - основной настроечный

import pytest
from src.config import settings
from src.database import BaseModelORM, engine_null_pull
from src.main import app
from src.models import *
from httpx import AsyncClient

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


#т.е запускать при каждом прогоне теста
@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_DB_main):
    print("Создание пользователя")
    async with AsyncClient(app=app, base_url="http://testuser") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "abc@mail.ru",
                "password": "123987",
                "name": "Test user"
            }
        )

#т.е запускать при каждом прогоне теста
@pytest.fixture(scope="session", autouse=True)
async def register_user(register_user):
    print("Создание тестовых данных")
    async with AsyncClient(app=app, base_url="http://testuser") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "abc@mail.ru",
                "password": "123987",
                "name": "Test user"
            }
        )

    