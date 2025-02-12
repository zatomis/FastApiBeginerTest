from datetime import date

from sqlalchemy import select

from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import Booking, BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking

    async def get_bookings_with_today_checkin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.schema.model_validate(booking, from_attributes=True) for booking in res.scalars().all()]

    async def add_booking(self, add_data:BookingAdd, hotel_id: int):
        """
        Добавление бронирования с ограничением на свободные номера
        Как отдельный метод. В начале - делаем запрос
        """
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=add_data.date_from,
            date_to=add_data.date_to,
            hotel_id=hotel_id,
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        # если такой номер есть, то добавляем
        if add_data.room_id in rooms_ids_to_book:
            new_booking = await self.add(add_data)
            return new_booking
        else:
            raise Exception





