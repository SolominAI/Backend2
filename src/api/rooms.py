from fastapi import Query, APIRouter, Path, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepositories
from src.schemas.rooms import RoomAdd, RoomPATCH

router = APIRouter(prefix='/hotel/{hotel_id}/room', tags=['Номера'])


@router.get('')
async def get_rooms(
        hotel_id: int = Path(..., description='ID отеля'),
        title: str | None = Query(None, description='Название номера'),
        price: int | None = Query(None, description='Цена'),
):
    async with async_session_maker() as session:
        return await RoomsRepositories(session).get_all(
            hotel_id=hotel_id,
            title=title,
            price=price
        )


@router.post('')
async def create_room(
        hotel_id: int = Path(..., description='ID отеля'),
        room_data: RoomAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        room = await RoomsRepositories(session).add_room(room_data, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK', 'data': room}


@router.get('/{room_id}')
async def get_room(
        hotel_id: int = Path(..., description='ID отеля'),
        room_id: int = Path(..., description='ID номера'),
):
    async with async_session_maker() as session:
        return await RoomsRepositories(session).get_one_or_none(
            id=room_id,
            hotel_id=hotel_id
        )


@router.put('/{room_id}')
async def edit_room(
        hotel_id: int = Path(..., description='ID отеля'),
        room_id: int = Path(..., description='ID номера'),
        room_data: RoomAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(
            data=room_data,
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
        return {'status': 'OK'}


@router.patch(
    '/{room_id}',
    summary='Частичное обновление номера',
    description='Обновление отдельных полей номера. Доступны title, description, price, quantity'
)
async def patch_room(
    hotel_id: int = Path(..., description='ID отеля'),
    room_id: int = Path(..., description='ID номера'),
    room_data: RoomPATCH = Body(...)
):
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(
            data=room_data,
            exclude_unset=True,
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    return {'status': 'OK'}


@router.delete('/{room_id}')
async def delete_room(
    hotel_id: int = Path(..., description='ID отеля'),
    room_id: int = Path(..., description='ID номера'),
):
    async with async_session_maker() as session:
        await RoomsRepositories(session).delete(
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    return {'status': 'OK'}
