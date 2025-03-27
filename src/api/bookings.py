from fastapi import APIRouter, Body
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest
from src.exceptions import (
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
)
from src.services.bookings import BookingServiceLayer


router = APIRouter(prefix="/bookings", tags=["Бронирование 🏪"])


@router.get(
    "/",
    summary="Запрос на бронь отелей",
    description="<H1>Получить данные о бронировании</H1>",
)
async def get_booking(db: DBDep):
    booking = await BookingServiceLayer(db).get_bookings()
    return {"status": "Ok", "data": booking}


@router.get(
    "/me",
    summary="Запрос на бронь отелей пользователя",
    description="<H1>Получить данные о бронировании номеров пользователя</H1>",
)
async def get_booking_me(user_id: UserIdDep, db: DBDep):
    booking = await BookingServiceLayer(db).get_my_bookings(user_id)
    return {"status": "Ok", "data": booking}


@router.post(
    "/",
    summary="Добавить бронирование номера",
    description="<H1>Добавить бронирование номера</H1>",
)
async def create_booking(
    db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest = Body()
):
    try:
        booking = await BookingServiceLayer(db).add_booking(
            user_id, booking_data
        )
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}
