from sqlalchemy import select, insert

from src.database import engine
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_all(self, hotel_id: int) -> list[Room]:
        query_room_statement = select(RoomsORM).where(RoomsORM.hotel_id == hotel_id)
        print(query_room_statement.compile(engine, compile_kwargs={"literal_binds": True}))
        query_result = await self.session.execute(query_room_statement)
        return [Room.model_validate(room, from_attributes=True) for room in query_result.scalars().all()]


    # async def add1(self, data: BaseModel, hotel_id: int):
    #     data["hotel_id"] = hotel_id
    #     add_statement = insert(self.model).values(**data.model_dump()).returning(self.model) #или .returning(self.model.id)-т.е. можно и одно поле
    #     print(add_statement.compile(engine, compile_kwargs={"literal_binds": True}))
    #     result = await self.session.execute(add_statement)
    #     model = result.scalars().one() #по результату итерируемся и вызывая метод-возвр.результат
    #     return self.schema.model_validate(model, from_attributes=True)
