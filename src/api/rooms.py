from datetime import date
from fastapi import APIRouter, Body, Query
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix='/hotels', tags=["Номера 🏬"])


@router.get("/{hotel_id}/rooms",
            summary="Запрос",
            description="<H1>Получить данные о номерах отеля по id</H1>")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-10-18"),
        date_to: date = Query(example="2024-12-18"),):

    room = await db.rooms.get_filter_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return {"status": "OK", "data": room}


@router.get("/{hotel_id}/room/{room_id}")
async def get_room(hotel_id: int,
                   room_id: int,
                   db: DBDep):
    room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}",
           summary="Удаление",
           description="<H1>Удалить комнату из отеля</H1>")
async def delete_room_in_hotel(hotel_id: int,
                               room_id: int,
                               db: DBDep):
    await db.rooms.remove(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}",
            summary="Обновление данных о комнате в отеле",
            description="<H1>Обновить данные о комнате в отеле</H1>")
async def put_room_in_hotel(hotel_id: int,
                            room_id: int,
                            db: DBDep,
                            room_data: RoomAddRequest): #room_data: RoomAddRequest - чтобы не трогать id
    _room_data = RoomAdd(hotel_id=hotel_id,
                         **room_data.model_dump()) #т.е. создали другую схему
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
           summary="Частичное обновление комнаты в отеле",
           description="<H1>Обновить данные о комнате частично</H1>")
async def patch_room(hotel_id: int,
                     room_id: int,
                     db: DBDep,
                     room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)) #exclude_unset-для того чтобы можно было бы делать только 1 поле
    await db.rooms.edit(_room_data,
                        exclude_unset=True,
                        hotel_id=hotel_id,
                        id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.post("/{hotel_id}/rooms",
           summary="Добавить данные о номере в отеле",
           description="<H1>Добавить номер в отель</H1>")
#принимаем без hotel id, но потом через _room_data прокинем, это чтобы меньше данных "гонять" по сети т.е. сократить их
async def create_room(hotel_id: int,
                      db: DBDep,
                      room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id,
                         **room_data.model_dump()) #т.е. создали другую схему
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}
