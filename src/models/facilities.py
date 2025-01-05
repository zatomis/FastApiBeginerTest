from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, String
from src.database import BaseModelORM
from src.models.rooms import RoomsORM


class FacilitiesORM(BaseModelORM):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    title: Mapped[str] = mapped_column(String(length=100))

    # это не столбец,а описание связи с таблицей М2М
    rooms: Mapped[list["RoomsORM"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities"
    )


class RoomFacilitiesORM(BaseModelORM):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
