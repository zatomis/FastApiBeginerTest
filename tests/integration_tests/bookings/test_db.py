from datetime import date
from pprint import pprint

from src.schemas.bookings import BookingAdd, Booking


#тут передаем фикстуру db, которая делает подключение к БД
#и тогда функция ниже - уже будет внутри контекстного менеджера
async def test_crud_booking(db):
    # Считаем кол-во данных до теста
    booking_count = await db.bookings.get_one_or_none()

    # взять данные для теста из БД
    user = (await db.users.get_all())[0]
    room = (await db.rooms.get_all())[0]

    booking_data = BookingAdd(
        user_id=user.id,
        room_id=room.id,
        date_from=date(year=2025, month=12, day=15),
        date_to=date(year=2025, month=12, day=19),
        price=1000,
    )
    new_booking = await db.bookings.add(booking_data)
    pprint(f"{new_booking.id=}")

    new_booking_id = await db.bookings.get_filter(id=new_booking.id)
    assert new_booking_id == new_booking_id

    patch_booking_data = Booking(
        user_id=user.id,
        room_id=room.id,
        date_from=date(year=2025, month=12, day=15),
        date_to=date(year=2025, month=12, day=19),
        price=1500,
    )

    await db.bookings.edit(patch_booking_data, id=new_booking_id)
    # await db.bookings.remove(id=new_booking_id)
    booking_count_after_test = await db.bookings.get_one_or_none()
    assert booking_count == booking_count_after_test

    await db.commit()