from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger
from src.database import BaseModelORM


class HotelsORM(BaseModelORM):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    title: Mapped[str] = mapped_column(String(length=100))
    location: Mapped[str] = mapped_column()
