from fastapi import Depends, Query  # зависимости
from pydantic import BaseModel
from typing import Annotated #это для своей типизации т.к. pydantic не связан с fastapi, но fastapi наоборот связан-это нужно чтобы правильно сделать Query

#перетаскивание из pydantic схем - в query параметры
class PaginationParams(BaseModel):
    page: Annotated[int | None ,  Query(1, gte=1, description="Страница")]
    per_page: Annotated[int | None ,  Query(3, lt=10, description="Кол-во")]

PaginationParamsDep = Annotated[PaginationParams, Depends()]