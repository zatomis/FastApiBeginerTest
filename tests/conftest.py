#спец файл для того чтобы при каждом прогоне
#тестов выполнялся. Файл настроечный - основной настроечный

import pytest
from src.config import settings
from src.database import BaseModelORM, engine_null_pull
from src.models import *


# автоматически запустить эту функцию но только для сессии т.е. один раз
# т.к. в самом начале тестов прогоняется именно этот файл - первым
# где удаляются и создаются тестовые таблицы
@pytest.fixture(scope="session", autouse=True)
async def async_main():
    print("Я ФИКСТУРА")
    assert settings.MODE == "TEST"
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(BaseModelORM.metadata.drop_all)
        await conn.run_sync(BaseModelORM.metadata.create_all)