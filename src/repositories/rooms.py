from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomAdd


class RoomsRepositories(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def add_room(self, data: RoomAdd, hotel_id: int):
        data_dict = data.model_dump()
        data_dict['hotel_id'] = hotel_id
        return await super().add(RoomAdd(**data_dict))
