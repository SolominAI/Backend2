import json

import pytest
from httpx import AsyncClient

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def insert_mock_hotels_and_rooms(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open("tests/mock_hotels.json", encoding="utf-8") as f:
            hotels_data = json.load(f)

        for hotel in hotels_data:
            await ac.post("/hotels", json=hotel)

        with open("tests/mock_rooms.json", encoding="utf-8") as f:
            rooms_data = json.load(f)

        for room in rooms_data:
            hotel_id = room.pop("hotel_id")
            await ac.post(f"/hotel/{hotel_id}/rooms", json=room)


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "1234"
            }
        )
