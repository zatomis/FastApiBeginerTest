from fastapi import APIRouter, Body
from src.repositories.rooms import RoomsRepository
from src.database import new_async_session_maker
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix='/hotels', tags=["Номера 🏪"])


@router.get("/{hotel_id}/rooms",
            summary="Запрос",
            description="<H1>Получить данные о номерах отеля по id</H1>")
async def get_rooms(hotel_id: int):
    async with (new_async_session_maker() as session):
        room = await RoomsRepository(session).get_filter(hotel_id=hotel_id)
    return {"status": "OK", "data": room}


@router.get("/{hotel_id}/room/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with (new_async_session_maker() as session):
        room = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}",
           summary="Удаление",
           description="<H1>Удалить комнату из отеля</H1>")
async def delete_room_in_hotel(hotel_id: int,
                               room_id: int):
    async with new_async_session_maker() as session:
        await RoomsRepository(session).remove(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}",
            summary="Обновление данных о комнате в отеле",
            description="<H1>Обновить данные о комнате в отеле</H1>")
async def put_room_in_hotel(hotel_id: int, room_id: int, room_data: RoomAddRequest): #room_data: RoomAddRequest - чтобы не трогать id
    _room_data = RoomAdd(hotel_id=hotel_id,
                         **room_data.model_dump()) #т.е. создали другую схему
    async with new_async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
           summary="Частичное обновление комнаты в отеле",
           description="<H1>Обновить данные о комнате частично</H1>")
async def patch_room(hotel_id: int,
                     room_id: int,
                     room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)) #exclude_unset-для того чтобы можно было бы делать только 1 поле
    async with new_async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data,
                                            exclude_unset=True,
                                            hotel_id=hotel_id,
                                            id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.post("/{hotel_id}/rooms",
           summary="Добавить данные о номере в отеле",
           description="<H1>Добавить номер в отель</H1>")
#принимаем без hotel id, но потом через _room_data прокинем, это чтобы меньше данных "гонять" по сети т.е. сократить их
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id,
                         **room_data.model_dump()) #т.е. создали другую схему
    async with new_async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}
