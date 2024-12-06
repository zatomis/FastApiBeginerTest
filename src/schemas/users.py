from pydantic import BaseModel, ConfigDict


class UserRequestAdd(BaseModel):
    email: str
    password: str
    name: str


class UserAdd(BaseModel):
    email: str
    hash_password: str
    name: str


class User(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(from_attributes=True)