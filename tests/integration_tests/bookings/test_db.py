from datetime import date

from src.schemas.bookings import BookingAdd, BookingPatch


#CRUD -> CREATE READ UPDATTR DELETE
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
    book = await db.bookings.add(booking_data)
    await db.commit()

    assert book.id is not None

    fetched = await db.bookings.get_one_or_none(id=book.id)
    assert fetched is not None
    assert fetched.price == 100

    await db.bookings.edit(BookingAdd(**booking_data.model_dump() | {"price": 200}), id=book.id)
    await db.commit()
    updated = await db.bookings.get_one_or_none(id=book.id)
    assert updated.price == 200

    await db.bookings.edit(BookingPatch(price=300), exclude_unset=True, id=book.id)
    await db.commit()
    patched = await db.bookings.get_one_or_none(id=book.id)
    assert patched.price == 300

    await db.bookings.delete(id=book.id)
    await db.commit()
    deleted = await db.bookings.get_one_or_none(id=book.id)
    assert deleted is None
