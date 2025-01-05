from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRelationShip


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filter_by_time(
            self,
            hotel_id,
            date_from,
            date_to):
        sql_query_rooms_id_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsORM.id.in_(sql_query_rooms_id_to_get))
        )
        res = await self.session.execute(query)
        return [RoomWithRelationShip.model_validate(model) for model in res.unique().scalars().all()]


