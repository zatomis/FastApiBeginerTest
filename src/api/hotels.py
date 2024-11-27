from fastapi import Query, APIRouter, Body

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import insert

from src.api.dependencies import PaginationParamsDep
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, HotelPatch
from src.database import new_async_session_maker

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubay", "name": "dubay"},
    {"id": 3, "title": "Moscow", "name": "moscow"},
    {"id": 4, "title": "Kazan", "name": "kazan"},
    {"id": 5, "title": "Rostov", "name": "rostov"},
    {"id": 6, "title": "Krosnodar", "name": "krd"},
]

router = APIRouter(prefix='/hotesl', tags=["Отели 🏨"])



@router.put("/{hotel_id}",
            summary="Полное обновление данных",
            description="<H1>Обновить данные об объекте</H1>")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            break
    else:
        return {"status": "Error id"}

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
        add_hotel_statement = insert(HotelsORM).values(**hotel_data.model_dump()) #тут из pydantic раскрывем в словарь, который вставим в БД
        await session.execute(add_hotel_statement)
        await session.commit()


    return {"status": "OK"}


@router.delete("/{hotel_id}",
           summary="Удаление",
           description="<H1>Удалить данные об объекте</H1>")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.get("",
           summary="Получить отели",
           description="<H1>Получить данные об объекте(ах)</H1>")
def get_hotels(
        paginations: PaginationParamsDep, #прокинуть в зависимости 2-а параметра page per_page
        id: int | None = Query(None, description="Просто id"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if paginations.page and paginations.per_page: #если параметры есть
        # , то
        return hotels_[paginations.per_page * (paginations.page-1) :][:paginations.per_page] #вернуть страницы с учетом того что уже могли бы быть страницы ранее
    else:
        return hotels_ #если их нет-вернуть всё
