from fastapi import APIRouter, Response
from starlette.responses import RedirectResponse
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService
from src.exceptions import (
    IncorrectPasswordHTTPException,
    IncorrectPasswordException,
    EmailNotRegisteredHTTPException,
    EmailNotRegisteredException,
    UserAlreadyExistsException,
    UserEmailAlreadyExistsHTTPException,
    PasswordEmptyException,
)

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    try:
        await AuthService(db).register_user(data)
    except PasswordEmptyException:
        raise IncorrectPasswordHTTPException
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
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


@router.get("/me", summary="Мои данные")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_one_or_none_user(user_id)


@router.get("/logout")
async def logout(
    response: Response,
):
    response = RedirectResponse("/logout", status_code=302)
    response.delete_cookie(key="access_token")
    return {"status": "OK"}
