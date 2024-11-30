from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import settings


# Команда для изменения кодировки: для DBeaver
#     SET client_encoding = 'UTF8';
#     UPDATE pg_database SET datcollate='ru_RU.UTF-8', datctype='ru_RU' WHERE datname='booking';
#     UPDATE pg_database set encoding = pg_char_to_encoding('UTF8') where datname = 'booking';
# После запуска команд не забудьть открыть новый SQL скрипт/редактор


# engine = create_async_engine(settings.DB_URL, echo=True)
engine = create_async_engine(settings.DB_URL, )
new_async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

class BaseModelORM(DeclarativeBase):
    """
    все данные о всех моделях
    """
    pass

# session = new_async_session_maker()
#     await session.execute()