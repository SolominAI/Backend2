from fastapi import Query, APIRouter, Path, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepositories
from src.schemas.rooms import RoomAdd

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


#
# @router.get("/{hotel_id}")
# async def get_hotel(hotel_id: int):
#     async with async_session_maker() as session:
#         return await HotelsRepositories(session).get_one_or_none(id=hotel_id)
#
#

#
#
# @router.put("/{hotel_id}")
# async def edit_hotel(
#     hotel_id: int,
#     hotel_data: HotelAdd = Body(
#         openapi_examples={
#             '1': {
#                 'summary': 'Сочи',
#                 'value': {
#                     'title': 'У моря',
#                     'location': 'г.Сочи, ул. Морская 222'
#                 }}
#         })
# ):
#
#     async with async_session_maker() as session:
#         await HotelsRepositories(session).edit(hotel_data, id=hotel_id)
#         await session.commit()
#
#     return {'status': 'OK'}
#
#
# @router.patch(
#     '/{hotel_id}',
#     summary='Патч данных отеля',
#     description='Ручка обновления параметров отеля по отдельности. Доступны title, name'
# )
# async def patch_hotel(
#         hotel_id: int,
#         hotel_data: HotelPATCH
# ):
#     async with async_session_maker() as session:
#         await HotelsRepositories(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
#         await session.commit()
#     return {'status': 'OK'}
#
#
# @router.delete('/{hotel_id}')
# async def delete_hotel(hotel_id: int):
#     async with async_session_maker() as session:
#         await HotelsRepositories(session).delete(id=hotel_id)
#         await session.commit()
#     return {'status': 'OK'}
