from fastapi import APIRouter

from src.database import new_async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(
        data: UserRequestAdd,
):
    hashed_passwd = ""
    new_user_data = UserAdd(email=data.email, hash_password=hashed_passwd)
    async with new_async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK", "data": user}
