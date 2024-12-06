from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import SmallInteger, String
from src.database import BaseModelORM


class UsersORM(BaseModelORM):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(String(200))
    password: Mapped[str] = mapped_column(String(200), unique=True)
    name: Mapped[str] = mapped_column(String(100))
