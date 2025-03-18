from datetime import date
from fastapi import APIRouter, Body, Query
from sqlalchemy.exc import IntegrityError
from fastapi import Response
from fastapi import HTTPException
from src.api.dependencies import DBDep
from src.exceptions import check_date_to_after_date_from, HotelNotFoundHTTPException, ObjectNotFoundException, \
    ObjectAlreadyExistsException, RoomNotFoundHTTPException
from src.schemas.facilities import RoomFaclityAdd
from src.schemas.rooms import (
    RoomPatch,
    RoomAdd,
    RoomAddRequest,
    RoomPatchWithFacilities,
)
from src.services.room import RoomServiceLayer

router = APIRouter(prefix="/hotels", tags=["Номера 🏬"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Запрос",
    description="<H1>Получить данные о номерах отеля по id</H1>",
)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-10-18"),
    date_to: date = Query(example="2024-12-18"),
):
    rooms = await RoomServiceLayer(db=db).get_filter_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )
    return {"status": "OK", "data": rooms}


@router.get("/{hotel_id}/room/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    room = await db.rooms.get_one_or_none_with_relations(
        hotel_id=hotel_id, id=room_id
    )
    if not room:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "room": room}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление",
    description="<H1>Удалить комнату из отеля</H1>",
)
async def delete_room_in_hotel(hotel_id: int, room_id: int, db: DBDep):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    await db.rooms.remove(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновление данных о комнате в отеле",
    description="<H1>Обновить данные о комнате в отеле</H1>",
)
async def put_room_in_hotel(
    hotel_id: int, room_id: int, db: DBDep, room_data: RoomAddRequest
):  # room_data: RoomAddRequest - чтобы не трогать id
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    _room_data = RoomAdd(
        hotel_id=hotel_id, **room_data.model_dump()
    )  # т.е. создали другую схему
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=room_data.facilities_ids
    )
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление комнаты в отеле",
    description="<H1>Обновить данные о комнате частично</H1>",
)
async def patch_room(
    hotel_id: int, room_id: int, db: DBDep, room_data: RoomPatchWithFacilities
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )  # exclude_unset-для того чтобы можно было бы делать только 1 поле
    await db.rooms.edit(
        _room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id
    )
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "OK"}


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавить данные о номере в отеле",
    description="<H1>Добавить номер в отель</H1>",
)
# принимаем без hotel id, но потом через _room_data прокинем, это чтобы меньше данных "гонять" по сети т.е. сократить их
async def create_room(
    hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()
):
    try:
        _room_data = RoomAdd(
            hotel_id=hotel_id,
            **room_data.model_dump(exclude={"facilities_ids"}),
        )  # исключили facilities_ids чтобы правильно сошлось по полям БД RoomsORM - там нет такого поля

        try:
            await db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundHTTPException
        try:
            room = await db.rooms.add(_room_data)
        except ObjectAlreadyExistsException:
            raise HTTPException(status_code=409, detail="Tакой уже существует")

        # создаем массив схем и одним методом выполняем
        rooms_facilities = [
            RoomFaclityAdd(room_id=room.id, facility_id=f_id)
            for f_id in room_data.facilities_ids
        ]

        if rooms_facilities:
            await db.rooms_facilities.add_bulk(rooms_facilities)
        await db.commit()
        return {"status": "OK", "data": rooms_facilities}
    except IntegrityError:
        return Response(
            {"msg": "Указанные удобства не найдены..."}, status_code=404
        )
