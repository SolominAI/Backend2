from datetime import date

from src.schemas.bookings import BookingAdd


# CRUD -> CREATE READ UPDATTR DELETE
async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=8, day=10),
        date_to=date(year=2026, month=8, day=20),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)
    await db.commit()

    assert new_booking.id is not None

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.price == 100

    updated_date = date(year=2026, month=8, day=25)
    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=8, day=10),
        date_to=updated_date,
        price=200,
    )

    await db.bookings.edit(update_booking_data, id=new_booking.id)
    update_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert update_booking
    assert update_booking.id == new_booking.id
    assert update_booking.date_to == updated_date

    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
