from datetime import date

from src.api.dependencies import PaginationDep
from src.exceptions import check_date_to__after_date_from
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtred_by_time(
            self,
            pagination: PaginationDep,
            title: str | None,
            location: str | None,
            date_from: date,
            date_to: date
    ):
        check_date_to__after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        offset = per_page * (pagination.page - 1)

        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
            limit=per_page,
            offset=offset,
        )

    async def get_hotel(self, hotel_id):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, data: HotelAdd):
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()

    async def edit_hotel_partially(self, hotel_id: int, data: HotelPatch, exclude_unset: bool = False):
        await self.db.hotels.edit(data, exclude_unset=exclude_unset, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()