from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Такой объект уже существует"


class EmptyValueException(NabronirovalException):
    detail = "Данные являются пустыми"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"


class RoomBadParameterHTTPException(NabronirovalHTTPException):
    status_code = 406
    detail = "Не верные переданные данные"


class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class IncorrectTokenHTTPException(NabronirovalHTTPException):
    detail = "Некорректный токен"


class EmailNotRegisteredHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class UserEmailAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class IncorrectPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Пароль неверный"


class NoAccessTokenHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"


class IncorrectTokenException(NabronirovalException):
    detail = "Некорректный токен"


class EmailNotRegisteredException(NabronirovalException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(NabronirovalException):
    detail = "Пароль неверный либо пустой"


class UserAlreadyExistsException(NabronirovalException):
    detail = "Пользователь уже существует"


class PasswordEmptyException(NabronirovalException):
    detail = "Пароль не может быть пустым"


class RoomNotFoundException(NabronirovalException):
    detail = "Номер не найден"


class HotelNotFoundException(NabronirovalException):
    detail = "Отель не найден"

