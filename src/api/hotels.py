from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select
from src.api.dependencies import PaginationParamsDep
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, HotelPatch
from src.database import new_async_session_maker, engine


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
        print(add_hotel_statement.compile(engine, compile_kwargs={"literal_binds": True}))
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
async def get_hotels(
        paginations: PaginationParamsDep, #прокинуть в зависимости 2-а параметра page per_page
        id: int | None = Query(None, description="Просто id"),
        title: str | None = Query(None, description="Название отеля"),
):
    async with new_async_session_maker() as session:
        limit = paginations.page
        offset = paginations.per_page * (paginations.page - 1)
        query_hotel_statement = (
            select(HotelsORM)
            .filter_by(id=id, title=title)
            .limit(limit)
            .offset(offset)
        )
        print(query_hotel_statement.compile(engine, compile_kwargs={"literal_binds": True}))
        query_result = await session.execute(query_hotel_statement)

        hotels = query_result.scalars().all() #из кортежей-> объекты отели
        return hotels
