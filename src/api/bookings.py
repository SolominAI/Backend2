from fastapi import APIRouter, Body, HTTPException
from src.schemas.bookings import BookingAdd, BookingAddRequest, BookingPatch
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Брони"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.get("/{booking_id}")
async def get_booking(booking_id: int, db: DBDep):
    return await db.bookings.get_one_or_none(id=booking_id)


@router.post("")
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Пример бронирования",
                "value": {
                    "date_from": "2025-05-14",
                    "date_to": "2025-05-20",
                    "room_id": 6,
                },
            }
        }
    ),
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    room_price: int = room.price
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.put("/{booking_id}")
async def edit_booking(
    booking_id: int,
    db: DBDep,
    booking_data: BookingAdd,
):
    await db.bookings.edit(booking_data, id=booking_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{booking_id}")
async def patch_booking(booking_id: int, db: DBDep, booking_data: BookingPatch):
    await db.bookings.edit(booking_data, exclude_unset=True, id=booking_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, db: DBDep):
    await db.bookings.delete(id=booking_id)
    await db.commit()
    return {"status": "OK"}
