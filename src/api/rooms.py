from datetime import date

from fastapi import APIRouter, Path, Body, Query

from src.api.dependencies import DBDep
from src.schemas.fasilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix='/hotel', tags=['Номера'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(
        db: DBDep,
        date_from: date = Query(example='2025-05-01'),
        date_to: date = Query(example='2025-05-15'),
        hotel_id: int = Path(..., description='ID отеля')
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(
        db: DBDep,
        hotel_id: int = Path(..., description='ID отеля'),
        room_id: int = Path(..., description='ID номера'),
):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post('/{hotel_id}/rooms/{room_id}')
async def create_room(
        db: DBDep,
        hotel_id: int = Path(..., description='ID отеля'),
        room_data: RoomAddRequest = Body(openapi_examples={
        '1': {'summary': 'Стандарт', 'value': {
            'title': 'Стандарт',
            'description': 'Стандартный номер с балконом',
            'price': 7000,
            'quantity': 15,
            "facilities_ids": [1, 2]
        }},
        '2': {'summary': 'Люкс', 'value': {
            'title': 'Люкс',
            'description': 'Просторный люкс с видом на море',
            'price': 15000,
            'quantity': 2
        }}
        })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]

    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {'status': 'OK', 'data': room}


@router.put('/{hotel_id}/rooms/{room_id}')
async def edit_room(
        db: DBDep,
        hotel_id: int = Path(..., description='ID отеля'),
        room_id: int = Path(..., description='ID номера'),
        room_data: RoomAddRequest = Body(openapi_examples={
        "1": {
            "summary": "Стандарт",
            "value": {
                "title": "Стандарт",
                "description": "Обновлённый номер после ремонта",
                "price": 7500,
                "quantity": 10
            }},
        "2": {
            "summary": "Люкс",
            "value": {
                "title": "Люкс",
                "description": "Полностью заменённый номер с джакузи",
                "price": 18000,
                "quantity": 3
            }}
        })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {'status': 'OK'}


@router.patch(
    '/{hotel_id}/rooms/{room_id}',
    summary='Частичное обновление номера',
    description='Обновление отдельных полей номера. Доступны title, description, price, quantity'
)
async def patch_room(
        db: DBDep,
        hotel_id: int = Path(..., description='ID отеля'),
        room_id: int = Path(..., description='ID номера'),
        room_data: RoomPatchRequest = Body(...)
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {'status': 'OK'}


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(
        db: DBDep,
        hotel_id: int = Path(..., description='ID отеля'),
        room_id: int = Path(..., description='ID номера'),
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {'status': 'OK'}
