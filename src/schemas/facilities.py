from pydantic import BaseModel, Field


class FaclitiesAdd(BaseModel):
    title: str


class Faclities(FaclitiesAdd):
    id: int
