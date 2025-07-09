from datetime import date

from fastapi import APIRouter, Path, Body, Query

from src.api.dependencies import DBDep
from src.exceptions import HotelNotFoundHTTPException, RoomNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotel", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    date_from: date = Query(example="2025-05-01"),
    date_to: date = Query(example="2025-05-15"),
    hotel_id: int = Path(..., description="ID отеля"),
):
    return await RoomService(db).get_filtered_by_time(date_from, date_to, hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    db: DBDep,
    hotel_id: int = Path(..., description="ID отеля"),
    room_id: int = Path(..., description="ID номера"),
):
    try:
        return await RoomService(db).get_room(room_id, hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int = Path(..., description="ID отеля"),
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Стандарт",
                "value": {
                    "title": "Стандарт",
                    "description": "Стандартный номер с балконом",
                    "price": 7000,
                    "quantity": 15,
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "Люкс",
                "value": {
                    "title": "Люкс",
                    "description": "Просторный люкс с видом на море",
                    "price": 15000,
                    "quantity": 2,
                },
            },
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    db: DBDep,
    hotel_id: int = Path(..., description="ID отеля"),
    room_id: int = Path(..., description="ID номера"),
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Стандарт",
                "value": {
                    "title": "Стандарт",
                    "description": "Обновлённый номер после ремонта",
                    "price": 7500,
                    "quantity": 10,
                },
            },
            "2": {
                "summary": "Люкс",
                "value": {
                    "title": "Люкс",
                    "description": "Полностью заменённый номер с джакузи",
                    "price": 18000,
                    "quantity": 3,
                    "facilities_ids": [1, 2],
                },
            },
        }
    ),
):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление номера",
    description="Обновление отдельных полей номера. Доступны title, description, price, quantity",
)
async def patch_room(
    db: DBDep,
    hotel_id: int = Path(..., description="ID отеля"),
    room_id: int = Path(..., description="ID номера"),
    room_data: RoomPatchRequest = Body(...),
):
    await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int = Path(..., description="ID отеля"),
    room_id: int = Path(..., description="ID номера"),
):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "OK"}
