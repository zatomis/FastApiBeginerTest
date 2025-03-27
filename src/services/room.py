from datetime import date
from src.exceptions import check_date_to_after_date_from
from src.services.base import BaseServiceLayer


class RoomServiceLayer(BaseServiceLayer):
    async def get_filter_by_time(
        self, hotel_id: int, date_from: date, date_to: date
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filter_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )


"""
from datetime import date

from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException, \
 \
    RoomNotFoundException

from src.schemas.facilities import RoomFacilityAdd

from src.schemas.rooms import RoomAddRequest, Room, RoomAdd, RoomPatchRequest, RoomPatch

from src.services.base import BaseService

from src.services.hotels import HotelService


class RoomService(BaseService):

    async def get_filtered_by_time(

            self,

            hotel_id: int,

            date_from: date,

            date_to: date,

    ):

        check_date_to_after_date_from(date_from, date_to)

        return await self.db.rooms.get_filtered_by_time(

            hotel_id=hotel_id, date_from=date_from, date_to=date_to

        )

    async def get_room(self, room_id: int, hotel_id: int):

        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)

    async def create_room(

            self,

            hotel_id: int,

            room_data: RoomAddRequest,

    ):

        try:

            await self.db.hotels.get_one(id=hotel_id)


        except ObjectNotFoundException as ex:

            raise HotelNotFoundException from ex

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

        room: Room = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [

            RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids

        ]

        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)

        await self.db.commit()

    async def edit_room(

            self,

            hotel_id: int,

            room_id: int,

            room_data: RoomAddRequest,

    ):

        await HotelService(self.db).get_hotel_with_check(hotel_id)

        await self.get_room_with_check(room_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

        await self.db.rooms.edit(_room_data, id=room_id)

        await self.db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)

        await self.db.commit()

    async def partially_edit_room(

            self,

            hotel_id: int,

            room_id: int,

            room_data: RoomPatchRequest,

    ):

        await HotelService(self.db).get_hotel_with_check(hotel_id)

        await self.get_room_with_check(room_id)

        _room_data_dict = room_data.model_dump(exclude_unset=True)

        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

        await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)

        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(

                room_id, facilities_ids=_room_data_dict["facilities_ids"]

            )

        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):

        await HotelService(self.db).get_hotel_with_check(hotel_id)

        await self.get_room_with_check(room_id)

        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)

        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:

        try:

            return await self.db.rooms.get_one(id=room_id)


        except ObjectNotFoundException:

            raise RoomNotFoundException
"""
