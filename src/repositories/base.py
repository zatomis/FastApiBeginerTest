from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from src.database import engine


class BaseRepository:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query_statement = select(self.model)
        print(query_statement.compile(engine, compile_kwargs={"literal_binds": True}))
        query_result = await self.session.execute(query_statement)
        return query_result.scalars().all()  # из кортежей-> объекты отели

    async def get_one_or_none(self, **filter_by):
        query_statement = select(self.model).filter_by(**filter_by)
        print(query_statement.compile(engine, compile_kwargs={"literal_binds": True}))
        query_result = await self.session.execute(query_statement)
        return query_result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_statement = insert(self.model).values(**data.model_dump()).returning(self.model) #или .returning(self.model.id)-т.е. можно и одно поле
        print(add_statement.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_statement)
        return result.scalars().one() #по результату итерируемся и вызывая метод-возвр.результат


    async def remove(self, id: int):
        del_statement = delete(self.model).where(self.model.id == id)
        print(del_statement.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(del_statement)


    async def edit(self, data: BaseModel, filter_id):
        update_statement = (
            update(self.model).
            where(self.model.id == filter_id).
            values(data.dict(exclude_unset=True))
        )
        print(update_statement.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(update_statement)
