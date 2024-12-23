from sqlalchemy import select, func
from src.database import engine
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filter_by_time(
            self,
            hotel_id,
            date_from,
            date_to):
        sql_query_rooms_id_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        # print(sql_query.compile(engine, compile_kwargs={"literal_binds": True}))
        #номера которые относятся к указанному отелю и не забронированы на текущие даты
        return await self.get_filter(RoomsORM.id.in_(sql_query_rooms_id_to_get))
