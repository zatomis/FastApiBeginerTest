from asyncpg import UniqueViolationError
from pydantic import BaseModel
from typing import Sequence, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError
from src.database import BaseModelORM
from sqlalchemy import select, insert, delete, update
from src.database import engine
from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException


class BaseRepository:
    model: type[BaseModelORM]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filter(self, *filter, **filter_by):
        query_statement = (
            select(self.model).filter(*filter).filter_by(**filter_by)
        )
        print(
            query_statement.compile(
                engine, compile_kwargs={"literal_binds": True}
            )
        )
        query_result = await self.session.execute(query_statement)
        # прошли по результату и преобразуем каждый элемент в схему pydantic т.о. выполняем DataMapper
        return [
            self.schema.model_validate(obj_model, from_attributes=True)
            for obj_model in query_result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs):
        return await self.get_filter()


    async def get_one_or_none(self, **filter_by):
        query_statement = select(self.model).filter_by(**filter_by)
        print(
            query_statement.compile(
                engine, compile_kwargs={"literal_binds": True}
            )
        )
        query_result = await self.session.execute(query_statement)
        model = query_result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)


    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.schema.model_validate(model, from_attributes=True)


    async def add_bulk(
        self, data: Sequence[BaseModel]
    ):  # принимаем массив список схем
        add_bulk_statement = insert(self.model).values(
            [item.model_dump() for item in data]
        )  # каждую схемку -> в словарик
        await self.session.execute(add_bulk_statement)

    async def add(self, data: BaseModel):
        try:
            add_statement = (
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )  # или .returning(self.model.id)-т.е. можно и одно поле
            # print(
            #     add_statement.compile(
            #         engine, compile_kwargs={"literal_binds": True}
            #     )
            # )
            result = await self.session.execute(add_statement)
            model = (
                result.scalars().one()
            )  # по результату итерируемся и вызывая метод-возвр.результат
            return self.schema.model_validate(model, from_attributes=True)
        except IntegrityError as ex:
            print(f"{type(ex.orig.__cause__)=}")
            if isinstance(ex.orig.__cause__, UniqueViolationError): #если классы ошибок совпали-то это именно про уникальность
                raise ObjectAlreadyExistsException from ex
            else:#иначе
                raise ex

    async def remove(self, **filter_by) -> None:
        del_statement = delete(self.model).filter_by(**filter_by)
        print(
            del_statement.compile(
                engine, compile_kwargs={"literal_binds": True}
            )
        )
        await self.session.execute(del_statement)

    async def remove_bulk(self, **filter_by):
        # remove_bulk_statement = delete(self.model).values([item.model_dump() for item in data]) #каждую схемку -> в словарик
        remove_bulk_statement = delete(self.model).filter_by(**filter_by)
        await self.session.execute(remove_bulk_statement)

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
        update_statement = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        print(
            update_statement.compile(
                engine, compile_kwargs={"literal_binds": True}
            )
        )
        await self.session.execute(update_statement)
