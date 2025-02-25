from pydantic import BaseModel, ConfigDict


class FaclitiesAdd(BaseModel):
    title: str


class Faclities(FaclitiesAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoomFaclityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFaclity(RoomFaclityAdd):
    id: int
    # model_config = ConfigDict(from_attributes=True)
