from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository


class HotelRepository(BaseRepository):
    model = HotelsORM