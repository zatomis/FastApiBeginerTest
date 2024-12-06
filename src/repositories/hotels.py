from sqlalchemy import select, func
from src.database import engine
from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel


class HotelRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    )-> list[Hotel]:

        query_hotel_statement = select(HotelsORM)
        if location:
            query_hotel_statement = query_hotel_statement.where(func.lower(HotelsORM.location).like(f'%{location.strip().lower()}%'))
        if title:
            query_hotel_statement = query_hotel_statement.where(func.lower(HotelsORM.title).like(f'%{title.strip().lower()}%'))
        query_hotel_statement = (
            query_hotel_statement
            .limit(limit)
            .offset(offset)
        )
        print(query_hotel_statement.compile(engine, compile_kwargs={"literal_binds": True}))
        query_result = await self.session.execute(query_hotel_statement)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in query_result.scalars().all()]
