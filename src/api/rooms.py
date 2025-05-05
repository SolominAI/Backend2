from fastapi import APIRouter, Path, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepositories
from src.schemas.rooms import RoomAdd, RoomPatchRequest, RoomPatch, RoomAddRequest

router = APIRouter(prefix='/hotel', tags=['Номера'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(
        hotel_id: int = Path(..., description='ID отеля'),
):
    async with async_session_maker() as session:
        return await RoomsRepositories(session).get_all(hotel_id=hotel_id)


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(
        hotel_id: int = Path(..., description='ID отеля'),
        room_id: int = Path(..., description='ID номера'),
):
    async with async_session_maker() as session:
        return await RoomsRepositories(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post('/{hotel_id}/rooms')
async def create_room(
        hotel_id: int = Path(..., description='ID отеля'),
        room_data: RoomAddRequest = Body(openapi_examples={
        '1': {'summary': 'Стандарт', 'value': {
            'title': 'Стандарт',
            'description': 'Стандартный номер с балконом',
            'price': 7000,
            'quantity': 15
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
    async with async_session_maker() as session:
        room = await RoomsRepositories(session).add(_room_data)
        await session.commit()

    return {'status': 'OK', 'data': room}


@router.put('/{hotel_id}/rooms/{room_id}')
async def edit_room(
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
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(_room_data, id=room_id)
        await session.commit()
        return {'status': 'OK'}


@router.patch(
    '/{hotel_id}/rooms/{room_id}',
    summary='Частичное обновление номера',
    description='Обновление отдельных полей номера. Доступны title, description, price, quantity'
)
async def patch_room(
    hotel_id: int = Path(..., description='ID отеля'),
    room_id: int = Path(..., description='ID номера'),
    room_data: RoomPatchRequest = Body(...)
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(
    hotel_id: int = Path(..., description='ID отеля'),
    room_id: int = Path(..., description='ID номера'),
):
    async with async_session_maker() as session:
        await RoomsRepositories(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}
