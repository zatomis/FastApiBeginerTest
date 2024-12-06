from fastapi import APIRouter
from passlib.context import CryptContext

from src.database import new_async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(
        data: UserRequestAdd,
):
    hashed_passwd = pwd_context.hash(data.password)

    async with (new_async_session_maker() as session):
        email = await UsersRepository(session).get_one_or_none(email=data.email)

    if email is None:
        new_user_data = UserAdd(email=data.email, password=hashed_passwd, name=data.name)
        async with new_async_session_maker() as session:
            user = await UsersRepository(session).add(new_user_data)
            await session.commit()
        return {"status": "OK", "data": user}
    else:
        return {"status": "Err. Email !!!"}
