from sqlalchemy import delete, select
from sqlalchemy.dialects.mysql import insert

from src.models.facilities import FacilitiesORM, RoomFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import Faclities, RoomFaclity


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Faclities


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesORM
    schema = RoomFaclity


    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        get_current_facilities_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ids: list[int] = res.scalars().all()
        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))
        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete),
                )
            )
            await self.session.execute(delete_m2m_facilities_stmt)
        if ids_to_insert:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])
            )
            await self.session.execute(insert_m2m_facilities_stmt)

    #задать/записать удобства номера
    async def set_room_faclities1(self, room_id: int, faclities_ids: list[int]):
        # только слолбец удобств
        get_facilities_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        current_res = await self.session.execute(get_facilities_ids_query)
        current_faclities_ids: list[int] = current_res.scalars().all()
        ids_to_delete: list[int] = list(set(current_faclities_ids) - set(faclities_ids))
        ids_to_add: list[int] = list(set(faclities_ids) - set(current_faclities_ids))

        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete)
                )
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_add:
            insert_m2m_facilities_stmt = (
                insert(self.model) #вставляем массив словарей
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_add]
                )
            )
            await self.session.execute(insert_m2m_facilities_stmt)
