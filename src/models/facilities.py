from datetime import date

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey, String
from src.database import BaseModelORM


class FacilitiesORM(BaseModelORM):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    title: Mapped[str] = mapped_column(String(length=100))


class RoomFacilitiesORM(BaseModelORM):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
