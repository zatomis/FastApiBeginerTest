from fastapi import Query, APIRouter, Body
from src.repositories.rooms import RoomsRepository
from src.database import new_async_session_maker, engine
from src.schemas.rooms import RoomPatch, RoomAdd

router = APIRouter(prefix='/hotels', tags=["Номера 🏪"])


@router.get("/{hotel_id}/rooms",
            summary="Запрос",
            description="<H1>Получить данные о номерах отеля по id</H1>")
async def get_rooms(hotel_id: int):
    async with (new_async_session_maker() as session):
        room = await RoomsRepository(session).get_all(hotel_id=hotel_id)
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/room/{room_id}",
           summary="Удаление",
           description="<H1>Удалить комнату из отеля</H1>")
async def delete_room_in_hotel(hotel_id: int, room_id: int):
    async with new_async_session_maker() as session:
        await RoomsRepository(session).remove(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/room/{room_id}",
            summary="Обновление данных о комнате в отеле",
            description="<H1>Обновить данные о комнате в отеле</H1>")
async def put_room_in_hotel(hotel_id: int, room_id: int, room_data: RoomPatch):
    async with new_async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/room/{room_id}",
           summary="Частичное обновление комнаты в отеле",
           description="<H1>Обновить данные о комнате частично</H1>")
async def patch_hotel(hotel_id: int, room_id: int, hotel_data: RoomPatch):
    async with new_async_session_maker() as session:
        await RoomsRepository(session).edit(hotel_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.post("/{hotel_id}/room",
           summary="Добавить данные о номере в отеле",
           description="<H1>Добавить номер в отель</H1>")
async def create_room(hotel_id: int, room_data: RoomAdd):
    async with new_async_session_maker() as session:
        room_data.hotel_id = hotel_id
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "room": room}
