from src.database import new_async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAdd(title="Hotel 3 stars", location="Сочи")
    async with DBManager(session_factory=new_async_session_maker_null_pool) as db:
        new_hotel = await db.hotels.add(hotel_data)
        print(f"f{new_hotel=}")