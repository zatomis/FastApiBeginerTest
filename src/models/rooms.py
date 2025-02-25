import typing
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, SmallInteger

from src.database import BaseModelORM

if typing.TYPE_CHECKING:
    from src.models.facilities import FacilitiesORM


class RoomsORM(BaseModelORM):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, unique=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None] #опциональный параметр
    price: Mapped[int]
    quantity: Mapped[int]

    #это не столбец,а описание связи с таблицей М2М
    facilities: Mapped[list["FacilitiesORM"]] = relationship(
        back_populates="rooms",
        secondary="rooms_facilities"
    )
