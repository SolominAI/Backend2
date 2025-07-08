from datetime import date

from src.exceptions import check_date_to__after_date_from, ObjectNotFoundException, HotelNotFoundException
from src.schemas.fasilities import RoomFacilityAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, Room
from src.services.base import BaseService


class RoomService(BaseService):
    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            hotel_id: int,
    ):
        check_date_to__after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, room_id: int, hotel_id: int):
        return await self.db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)

    async def create_room(
            self,
            hotel_id: int,
            room_data: RoomAddRequest,
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room: Room = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
                ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
