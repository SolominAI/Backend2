from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper

from src.repositories.base import BaseRepository


class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper
