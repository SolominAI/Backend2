from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomAdd, RoomCreate


class RoomsRepositories(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self,
                      hotel_id: int,
                      title: str | None = None,
                      price: int | None = None) -> list[Room]:
        query = select(RoomsOrm).where(RoomsOrm.hotel_id == hotel_id)

        if title:
            query = query.where(func.lower(RoomsOrm.title).contains(title.strip().lower()))

        if price:
            query = query.where(RoomsOrm.price == price)

        result = await self.session.execute(query)

        return [self.schema.model_validate(room, from_attributes=True) for room in result.scalars().all()]

    async def add_room(self, data: RoomAdd, hotel_id: int):
        data_dict = data.model_dump()
        data_dict['hotel_id'] = hotel_id
        return await super().add(RoomCreate(**data_dict))
