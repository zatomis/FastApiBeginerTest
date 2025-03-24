from datetime import date
from fastapi_cache.decorator import cache
from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationParamsDep, DBDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotel import HotelServiceLayer

router = APIRouter(prefix="/hotels", tags=["Отели 🏨"])


@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных",
    description="<H1>Обновить данные об объекте</H1>",
)
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep,
):
    try:
        if await db.hotels.get_one(id=hotel_id):
            await db.hotels.edit(hotel_data, id=hotel_id)
            await db.commit()
            return {"status": "OK"}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление",
    description="<H1>Обновить данные об объекте</H1>",
)
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    try:
        if await db.hotels.get_one(id=hotel_id):
            await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
            await db.commit()
            return {"status": "OK"}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.delete(
    "/{hotel_id}",
    summary="Удаление",
    description="<H1>Удалить данные об объекте</H1>",
)
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        if await db.hotels.get_one(id=hotel_id):
            await db.hotels.remove(id=hotel_id)
            await db.commit()
            return {"status": "OK"}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.get(
    "/{hotel_id}",
    summary="Запрос",
    description="<H1>Получить данные об одном отели по id</H1>",
)
@cache(expire=30)
async def get_by_id(hotel_id: int, db: DBDep):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.get(
    "",
    summary="Получить отели",
    description="<H1>Получить данные об объекте(ах)</H1>",
)
@cache(expire=30)
async def get_hotels(
    paginations: PaginationParamsDep,  # прокинуть в зависимости 2-а параметра page per_page
    db: DBDep,
    location: str | None = Query(None, description="Местоположение отеля"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2024-10-18"),
    date_to: date = Query(example="2024-12-18"),
):
    hotel = await HotelServiceLayer(db=db).get_filter_by_time(
        paginations=paginations,
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to
    )
    return {"status": "OK", "data": hotel}



@router.post(
    "/", summary="Добавить данные", description="<H1>Добавить отель</H1>"
)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Морское Сочи 5зв.",
                    "location": "ул.Моря 152А",
                },
            },
            "2": {
                "summary": "Княжий отель в степи",
                "value": {
                    "title": "Княжий отель в степи",
                    "location": "пер. Степной 18",
                },
            },
        }
    ),
):
    hotel_data.title = hotel_data.title.strip()
    hotel_data.location = hotel_data.location.strip()
    if hotel_data.title != '' and hotel_data.location != '':
        if not await db.hotels.get_filter(title=hotel_data.title, location=hotel_data.location):
            hotel = await db.hotels.add(hotel_data)
            await db.commit()
            return {"status": "OK", "data": hotel}
        else:
            return {"status": "Такой отель уже есть"}
    else:
        return {"status": 'Название или местоположение не должны быть пустые! '}
