from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException, Response

from src.config import settings
from src.database import new_async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

import jwt

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)#время жизни токена
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


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
        if not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail=f"Пароль не верный ! ")

        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
