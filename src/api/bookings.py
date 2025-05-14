from fastapi import APIRouter, Body, HTTPException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependencies import DBDep

router = APIRouter(prefix='/bookings', tags=['Брони'])


@router.post('')
async def create_booking(
    db: DBDep,
    booking_data: BookingAddRequest = Body(openapi_examples={
            '1': {'summary': 'Пример бронирования', 'value': {
                'date_from': '2025-05-14',
                'date_to': '2025-05-20',
                'room_id': 6
            }}
        }),
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if room is None:
        raise HTTPException(status_code=404, detail='Комната не найдена')

    booking = await db.bookings.add(BookingAdd(price=room.price, **booking_data.model_dump()))
    await db.commit()
    return {"status": "OK", "data": booking}
