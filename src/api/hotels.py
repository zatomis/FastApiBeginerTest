from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationParamsDep, DBDep
from src.repositories.hotels import HotelRepository
from src.schemas.hotels import HotelPatch, HotelAdd
from src.database import new_async_session_maker


router = APIRouter(prefix='/hotels', tags=["Отели 🏨"])


@router.put("/{hotel_id}",
            summary="Полное обновление данных",
            description="<H1>Обновить данные об объекте</H1>")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with new_async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частичное обновление",
           description="<H1>Обновить данные об объекте</H1>")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    async with new_async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}",
           summary="Удаление",
           description="<H1>Удалить данные об объекте</H1>")
async def delete_hotel(hotel_id: int):
    async with new_async_session_maker() as session:
        await HotelRepository(session).remove(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.get("/{hotel_id}",
            summary="Запрос",
            description="<H1>Получить данные об одном отели по id</H1>")
async def get_by_id(hotel_id: int):
    async with (new_async_session_maker() as session):
        hotel = await HotelRepository(session).get_one_or_none(id=hotel_id)
    return {"status": "OK", "data": hotel}


@router.get("",
           summary="Получить отели",
           description="<H1>Получить данные об объекте(ах)</H1>")
async def get_hotels(
        paginations: PaginationParamsDep, #прокинуть в зависимости 2-а параметра page per_page
        db: DBDep,
        location: str | None = Query(None, description="Местоположение отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = paginations.per_page or 3
    return db.hotels.get_all(
        location = location,
        title = title,
        limit = per_page,
        offset = (per_page * (paginations.page - 1))
    )


@router.post("/",
           summary="Добавить данные",
           description="<H1>Добавить отель</H1>")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
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
