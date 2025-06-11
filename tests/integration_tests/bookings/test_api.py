import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2026-08-01", "2026-08-10", 200),
    (1, "2026-08-02", "2026-08-08", 200),
    (1, "2026-08-03", "2026-08-04", 200),
    (1, "2026-08-03", "2026-08-11", 200),
    (1, "2026-08-01", "2026-08-09", 200),
    (1, "2026-08-01", "2026-08-10", 500),
    (1, "2026-09-01", "2026-09-10", 200)
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_ac
):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    print(f"{response.json()=}")

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res['status'] == "OK"
        assert "data" in res
