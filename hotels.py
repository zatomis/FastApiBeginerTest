from fastapi import Query, APIRouter, Body

from schemas.hotels import Hotel, HotelPatch


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
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи",
          "value":
              {"title": "Отель Сочи 5зв.",
               "name": "sochi"}
          },
    "2": {"summary": "Княжий отель",
          "value":
              {"title": "Khan hotel",
               "name": "loga"}
          },

})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": str(hotel_data.name).lower()
    })
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
        id: int | None = Query(None, description="Просто id"),
        title: str | None = Query(None, description="Название отеля"),
        page: int | None = Query(1, description="Страница"),
        page_quantity: int | None= Query(3, description="Кол-во"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if hotels_:
        return hotels_[page:page_quantity]
    else:
        return {"status": "Empty"}

