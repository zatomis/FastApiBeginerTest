from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserAdd(BaseModel):
    email: EmailStr
    password: str
    name: str


class User(BaseModel):
    id: int
    email: EmailStr
    name: str
    model_config = ConfigDict(from_attributes=True)


class UserWithHashPassword(User):
    # hash_password: str
    password: str
