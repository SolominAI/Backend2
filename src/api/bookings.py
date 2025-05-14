from fastapi import APIRouter, Body, HTTPException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix='/bookings', tags=['Брони'])


@router.get('')
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get('/me')
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post('')
async def create_booking(
    user_id: UserIdDep,
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

    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
