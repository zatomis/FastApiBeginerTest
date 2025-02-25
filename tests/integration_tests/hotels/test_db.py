from pprint import pprint
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


# тут передаем фикстуру, которая делает подключение к БД
# и тогда функция ниже - уже будет внутри контекстного менеджера
async def test_add_hotel(db: DBManager):
    hotel_data = HotelAdd(title="Hotel 3 stars", location="Сочи")
    new_hotel = await db.hotels.add(hotel_data)
    pprint(f"f{new_hotel=}")
    await db.commit()
