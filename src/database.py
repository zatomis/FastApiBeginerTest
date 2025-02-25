from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import settings


# Команда для изменения кодировки: для DBeaver
#     SET client_encoding = 'UTF8';
#     UPDATE pg_database SET datcollate='ru_RU.UTF-8', datctype='ru_RU' WHERE datname='booking';
#     UPDATE pg_database set encoding = pg_char_to_encoding('UTF8') where datname = 'booking';
# После запуска команд не забудьть открыть новый SQL скрипт/редактор


# db_params = {}
# if settings.MODE == "TEST":
#     db_params = {"poolclass": NullPool}

# engine = create_async_engine(settings.DB_URL, echo=True)
# engine = create_async_engine(settings.DB_URL, **db_params)
engine = create_async_engine(settings.DB_URL)
engine_null_pull = create_async_engine(
    settings.DB_URL, poolclass=NullPool
)  # единичное соединение для celery

new_async_session_maker = async_sessionmaker(
    bind=engine, expire_on_commit=False
)
new_async_session_maker_null_pool = async_sessionmaker(
    bind=engine_null_pull, expire_on_commit=False
)


class BaseModelORM(DeclarativeBase):
    """
    все данные о всех моделях
    """

    pass


# session = new_async_session_maker()
#     await session.execute()
