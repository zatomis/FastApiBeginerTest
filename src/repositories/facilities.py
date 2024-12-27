from src.models.facilities import FacilitiesORM, RoomFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import Faclities, RoomFaclity


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Faclities


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesORM
    schema = RoomFaclity

