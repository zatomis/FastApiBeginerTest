import jwt
from fastapi import APIRouter, Body
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix='/bookings', tags=["Бронирование 🏪"])

@router.post("/",
           summary="Добавить бронирование номера",
           description="<H1>Добавить бронирование номера</H1>")
async def create_booking(db: DBDep,
                         user_id: UserIdDep,
                         booking_data: BookingAddRequest = Body()):

    # jwt.exceptions.ExpiredSignatureError
    try:
        hotel_id = await db.rooms.get_one_or_none(id=booking_data.room_id)
        if hotel_id:
            user = await db.users.get_one_or_none(id=user_id)
            _booking_data = BookingAdd(user_id=user.id,
                                       price=1000,
                                       **booking_data.model_dump())
            booking = await db.bookings.add(_booking_data)
            await db.commit()
            return {"status": "OK", "data": booking}
        else:
            return {"status": "Bad", "data": hotel_id}
    except jwt.ExpiredSignature:
        return {"status": "Bad"}