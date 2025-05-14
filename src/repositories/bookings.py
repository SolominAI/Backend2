from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking
from src.repositories.base import BaseRepository


class BookingRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
