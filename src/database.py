from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.util.preloaded import engine_result

from src.config import settings

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