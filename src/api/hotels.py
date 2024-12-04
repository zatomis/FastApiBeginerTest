from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select, func
from sqlalchemy.sql.functions import session_user
from sqlalchemy.util import await_only

from src.api.dependencies import PaginationParamsDep
from src.models.hotels import HotelsORM
from src.repositories.hotels import HotelRepository
from src.schemas.hotels import Hotel, HotelPatch
from src.database import new_async_session_maker, engine


router = APIRouter(prefix='/hotesl', tags=["Отели 🏨"])


@router.put("/{hotel_id}",
            summary="Полное обновление данных",
            description="<H1>Обновить данные об объекте</H1>")
async def put_hotel(hotel_id: int, hotel_data: Hotel):
    async with new_async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частичное обновление",
           description="<H1>Обновить данные об объекте</H1>")
def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            break
    return {"status": "OK"}


@router.delete("/{hotel_id}",
           summary="Удаление",
           description="<H1>Удалить данные об объекте</H1>")
async def delete_hotel(hotel_id: int):
    async with new_async_session_maker() as session:
        hotel = await HotelRepository(session).remove(hotel_id)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.get("",
           summary="Получить отели",
           description="<H1>Получить данные об объекте(ах)</H1>")
async def get_hotels(
        paginations: PaginationParamsDep, #прокинуть в зависимости 2-а параметра page per_page
        location: str | None = Query(None, description="Местоположение отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = paginations.per_page or 3
    async with (new_async_session_maker() as session):
        return await HotelRepository(session).get_all(
            location = location,
            title = title,
            limit = per_page,
            offset = (per_page * (paginations.page - 1))
        )

@router.post("/",
           summary="Добавить данные",
           description="<H1>Добавить отель</H1>")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи",
          "value":
              {"title": "Отель Морское Сочи 5зв.",
               "location": "ул.Моря 152А"}
          },
    "2": {"summary": "Княжий отель в степи",
          "value":
              {"title": "Княжий отель в степи",
               "location": "пер. Степной 18"}
          },

})
):
    #откр.транзакцию
    async with new_async_session_maker() as session:
        hotel = await HotelRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}
