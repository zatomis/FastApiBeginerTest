from datetime import date

from src.exceptions import check_date_to_after_date_from
from src.services.base import BaseServiceLayer


class RoomServiceLayer(BaseServiceLayer):
    async def get_filter_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filter_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

