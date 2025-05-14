from datetime import date
from pydantic import BaseModel, ConfigDict


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingAdd(BaseModel):
    date_from: date
    date_to: date
    room_id: int
    price: int
    user_id: int = 4  # отложили реализацию


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)