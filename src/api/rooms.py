from datetime import date
from fastapi import APIRouter, Body, Query
from sqlalchemy.exc import IntegrityError
from fastapi import Response
from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFaclityAdd
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatchWithFacilities

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
    facilities = await db.rooms_facilities.get_filter(room_id=room.id)
    data_room = {"data": room}
    data_room["facilities"] = [facilities_room.facility_id for facilities_room in facilities]
    return {"status": "OK", "room":data_room}


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
    #удалить все удобства
    await db.rooms_facilities.remove(room_id=room_id)
    #добавить новые
    rooms_facilities = [RoomFaclityAdd(room_id=room_id,
                                       facility_id=f_id)
                        for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
           summary="Частичное обновление комнаты в отеле",
           description="<H1>Обновить данные о комнате частично</H1>")
async def patch_room(hotel_id: int,
                     room_id: int,
                     db: DBDep,
                     # room_data: RoomPatchRequest): было так
                     room_data: RoomPatchWithFacilities):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)) #exclude_unset-для того чтобы можно было бы делать только 1 поле
    await db.rooms.edit(_room_data,
                        exclude_unset=True,
                        hotel_id=hotel_id,
                        id=room_id)
    patch_facilities = set(room_data.facilities_ids)
    current_facilities = set([cf.facility_id for cf in await db.rooms_facilities.get_filter(room_id=room_id)])
    # находим пересечение,
    # если путое,
    #  то удалить те что есть и добавить все новые удобства
    # иначе
    #  из текущих вычитаем результат пересечения и это удаляем
    #  а из исходных вычитая результат пересечения - их добавить
    intersection = patch_facilities & current_facilities
    if intersection:
        facilities_for_delete = list(current_facilities - intersection)
        rooms_facilities_del = [RoomFaclityAdd(room_id=room_id,
                                           facility_id=f_id)
                            for f_id in facilities_for_delete]
        # await db.rooms_facilities.remove_bulk(rooms_facilities_del)
        for facilities_del in rooms_facilities_del:
            await db.rooms_facilities.remove(room_id=room_id, facility_id=facilities_del.facility_id)

        facilities_add_new = list(patch_facilities - intersection)
        rooms_facilities_add = [RoomFaclityAdd(room_id=room_id,
                                           facility_id=f_id)
                            for f_id in facilities_add_new]
        await db.rooms_facilities.add_bulk(rooms_facilities_add)
    else:
        # удалить те что были ранее т.к. их нет в запросе
        await db.rooms_facilities.remove(room_id=room_id)
        # добавить новые из запроса
        rooms_facilities = [RoomFaclityAdd(room_id=room_id,
                                           facility_id=f_id)
                            for f_id in room_data.facilities_ids]
        await db.rooms_facilities.add_bulk(rooms_facilities)

    await db.commit()
    return {"status": "OK"}


@router.post("/{hotel_id}/rooms",
           summary="Добавить данные о номере в отеле",
           description="<H1>Добавить номер в отель</H1>")
#принимаем без hotel id, но потом через _room_data прокинем, это чтобы меньше данных "гонять" по сети т.е. сократить их
async def create_room(hotel_id: int,
                      db: DBDep,
                      room_data: RoomAddRequest = Body()):
    try:
        _room_data = RoomAdd(hotel_id=hotel_id,
                             **room_data.model_dump(exclude={"facilities_ids"})) #исключили facilities_ids чтобы правильно сошлось по полям БД RoomsORM - там нет такого поля
        room = await db.rooms.add(_room_data)
        #создаем массив схем и одним методом выполняем
        rooms_facilities = [RoomFaclityAdd(room_id=room.id,
                                           facility_id=f_id)
                            for f_id in room_data.facilities_ids]

        await db.rooms_facilities.add_bulk(rooms_facilities)
        await db.commit()
        return {"status": "OK", "data": rooms_facilities}
    except IntegrityError:
        return Response({"msg": "Указанные удобства не найдены..."}, status_code=404)
