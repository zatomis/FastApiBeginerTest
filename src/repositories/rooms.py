from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
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


    async def get_one_or_none_with_relations(self, **filter_by):
        query_statement = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        query_result = await self.session.execute(query_statement)
        model = query_result.scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRelationShip.model_validate(model, from_attributes=True)



