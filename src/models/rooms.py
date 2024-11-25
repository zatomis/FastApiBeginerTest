from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, SmallInteger

from src.database import BaseModelORM


class RoomsORM(BaseModelORM):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, unique=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None] #опциональный параметр
    price: Mapped[int]
    quantity: Mapped[int]
