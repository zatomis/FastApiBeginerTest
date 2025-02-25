from pydantic import BaseModel, ConfigDict

from src.schemas.facilities import Faclities


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = (
        None  # если поле опиционально-то обязательно должно быть значение для него задано
    )
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    title: str
    description: str | None = (
        None  # если поле опиционально-то обязательно должно быть значение для него задано
    )
    price: int
    quantity: int
    hotel_id: int


class Room(RoomAdd):
    id: int
    # параметр ниже для того чтобы легко приводить ответы алфимии к схеме Pydantic
    model_config = ConfigDict(from_attributes=True)


class RoomWithRelationShip(Room):
    facilities: list[Faclities]


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None  # т.е. опционально
    price: int | None = None
    quantity: int | None = None


class RoomPatch(RoomPatchRequest):
    hotel_id: int | None = None


class RoomPatchWithFacilities(RoomPatchRequest):
    facilities_ids: list[int] = []
