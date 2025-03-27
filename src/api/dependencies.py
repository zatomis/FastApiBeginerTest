from fastapi import Depends, Query, Request  # зависимости
from pydantic import BaseModel
from typing import (
    Annotated,
)  # это для своей типизации т.к. pydantic не связан с fastapi, но fastapi наоборот связан-это нужно чтобы правильно сделать Query

from src.database import new_async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.exceptions import (
    IncorrectTokenException,
    IncorrectTokenHTTPException,
    NoAccessTokenHTTPException,
)


# перетаскивание из pydantic схем - в query параметры
class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, gte=1, description="Страница")]
    per_page: Annotated[int | None, Query(3, lt=10, description="Кол-во")]


PaginationParamsDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise NoAccessTokenHTTPException
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().decode_jwt_token(token)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=new_async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
