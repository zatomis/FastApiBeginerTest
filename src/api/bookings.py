import jwt
from fastapi import APIRouter, Body
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование 🏪"])


@router.get(
    "/",
    summary="Запрос на бронь отелей",
    description="<H1>Получить данные о бронировании</H1>",
)
async def get_booking(db: DBDep):
    booking = await db.bookings.get_all()
    return {"status": "Ok", "data": booking}


@router.get(
    "/me",
    summary="Запрос на бронь отелей пользователя",
    description="<H1>Получить данные о бронировании номеров пользователя</H1>",
)
async def get_booking_me(user_id: UserIdDep, db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    booking = await db.bookings.get_filter(user_id=user.id)
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
        hotel_id = await db.rooms.get_one_or_none(id=booking_data.room_id)
        if hotel_id:
            user = await db.users.get_one_or_none(id=user_id)
            room = await db.rooms.get_one_or_none(id=booking_data.room_id)
            hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
            room_price = room.price
            _booking_data = BookingAdd(
                user_id=user.id, price=room_price, **booking_data.model_dump()
            )
            booking = await db.bookings.add_booking(
                _booking_data, hotel_id=hotel.id
            )
            await db.commit()
            return {"status": "OK", "data": booking}
        else:
            return {"status": "Bad", "data": hotel_id}
    except jwt.ExpiredSignature or jwt.ExpiredSignatureError:
        return {"status": "Bad"}
