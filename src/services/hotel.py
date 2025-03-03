from datetime import date

from src.api.dependencies import PaginationParamsDep
from src.exceptions import check_date_to_after_date_from
from src.services.base import BaseServiceLayer

# выносим в этот класс методы из api
class HotelServiceLayer(BaseServiceLayer):
    async def get_filter_by_time(
            self,
            paginations: PaginationParamsDep,  # прокинуть в зависимости 2-а параметра page per_page
            location: str | None,
            title: str | None,
            date_from: date,
            date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = paginations.per_page or 3
        return await self.db.hotels.get_filter_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (paginations.page - 1),
        )