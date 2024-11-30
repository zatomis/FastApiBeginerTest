from sqlalchemy import select

from src.database import engine



class BaseRepository:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query_hotel_statement = select(self.model)
        print(query_hotel_statement.compile(engine, compile_kwargs={"literal_binds": True}))
        query_result = await self.session.execute(query_hotel_statement)
        return query_result.scalars().all()  # из кортежей-> объекты отели

    async def get_one_or_none(self, **filter_by):
        query_hotel_statement = select(self.model).filter_by(**filter_by)
        print(query_hotel_statement.compile(engine, compile_kwargs={"literal_binds": True}))
        query_result = await self.session.execute(query_hotel_statement)
        return query_result.scalars().one_or_none()
