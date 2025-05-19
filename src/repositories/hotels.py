from datetime import date

from sqlalchemy import select, func

from src.database import engine
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            title: str | None = None,
            location: str | None = None,
            limit: int = 5,
            offset: int = 0,
            hotel_id: int | None = None
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id
        )

        print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = (
            select(self.model).filter(self.model.id.in_(hotels_ids_to_get))
        )

        if title:
            query = query.filter(func.lower(self.model.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(self.model.location).contains(location.strip().lower()))

        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
