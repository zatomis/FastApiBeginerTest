from fastapi import APIRouter, HTTPException, Response
from src.database import new_async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd,
):
    hashed_passwd = AuthService().hash_password(data.password)

    async with (new_async_session_maker() as session):
        email = await UsersRepository(session).get_one_or_none(email=data.email)

    if email is None:
        new_user_data = UserAdd(email=data.email, password=hashed_passwd, name=data.name)
        async with new_async_session_maker() as session:
            user = await UsersRepository(session).add(new_user_data)
            await session.commit()
        return {"status": "OK", "data": user}
    else:
        return {"status": "Error. Dublicate Email !!!",
                "data": email}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):

    async with (new_async_session_maker() as session):
        user = await UsersRepository(session).get_user_hash_pwd(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail=f"Нет такого пользователя с {data.email} ! ")

        #проверим пароль юзера
        if not AuthService().verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail=f"Пароль не верный ! ")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
