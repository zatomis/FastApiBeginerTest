from datetime import date
from src.schemas.bookings import BookingAdd, Booking
from src.utils.db_manager import DBManager


# тут передаем фикстуру db, которая делает подключение к БД
# и тогда функция ниже - уже будет внутри контекстного менеджера
async def test_crud_booking(db: DBManager):
    # Считаем кол-во данных до теста
    # await db.bookings.get_one_or_none()

    # взять данные для теста из БД
    user = (await db.users.get_all())[0]  # type: ignore
    room = (await db.rooms.get_all())[0]  # type: ignore

    booking_data = BookingAdd(
        user_id=user.id,
        room_id=room.id,
        date_from=date(year=2025, month=12, day=15),
        date_to=date(year=2025, month=12, day=19),
        price=1000,
    )
    new_booking: Booking = await db.bookings.add(booking_data)

    new_booking_id = await db.bookings.get_filter(id=new_booking.id)
    assert new_booking_id
    assert new_booking_id == new_booking_id

    # обновить бронь
    updated_date = date(year=2024, month=8, day=25)
    update_booking_data = BookingAdd(
        user_id=user.id,
        room_id=room.id,
        date_from=date(year=2024, month=8, day=10),
        date_to=updated_date,
        price=100,
    )

    await db.bookings.edit(update_booking_data, id=new_booking.id)

    updated_booking: Booking | None = await db.bookings.get_one_or_none(
        id=new_booking.id
    )
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == updated_date
    # удалить бронь
    await db.bookings.remove(id=new_booking.id)
    booking: Booking | None = await db.bookings.get_one_or_none(
        id=new_booking.id
    )
    assert not booking

    await db.commit()
