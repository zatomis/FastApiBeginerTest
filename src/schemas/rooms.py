from pydantic import BaseModel, Field


class Room(BaseModel):
    id: int
    title: str
    description: str
    price: int
    quantity: int


class RoomPatch(BaseModel):
    description: str | None = Field(None)
    price: int | None = Field(None)


class RoomAdd(BaseModel):
    description: str
    price: int
    title: str
    quantity: int
    hotel_id: int
