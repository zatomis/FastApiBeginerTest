from fastapi import APIRouter, HTTPException, Response
from starlette.responses import RedirectResponse
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    hashed_passwd = AuthService().hash_password(data.password)
    email = await db.users.get_one_or_none(email=data.email)

    if email is None:
        new_user_data = UserAdd(
            email=data.email, password=hashed_passwd, name=data.name
        )
        user = await db.users.add(new_user_data)
        await db.commit()
        return {"status": "OK", "data": user}
    else:
        return {"status": "Error. Dublicate Email !!!", "data": email}


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
    user = await db.users.get_user_hash_pwd(email=data.email)
    if not user:
        raise HTTPException(
            status_code=401, detail=f"Нет такого пользователя с {data.email} ! "
        )

    # проверим пароль юзера
    if not AuthService().verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Пароль не верный !")

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


async def get_access_token(request):
    access_token = None
    cookie = dict(request.headers.items())["cookie"].split(";")
    for token in cookie:
        str_token = token.split("=")
        if str_token[0].strip() == "access_token":
            access_token = str_token[1].strip()
    return access_token


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await db.users.get_one_or_none(id=user_id)


@router.get("/logout")
async def logout(
    response: Response,
):
    response = RedirectResponse("/logout", status_code=302)
    response.delete_cookie(key="access_token")
    return response
