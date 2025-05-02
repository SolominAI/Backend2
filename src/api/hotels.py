from fastapi import Query, APIRouter, Body

from src.repositories.hotels import HotelsRepositories
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import HotelPATCH, HotelAdd


router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Местоположения и адрес'),
):

    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepositories(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepositories(session).get_one_or_none(id=hotel_id)


@router.post('')
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value': {
        'title': 'У моря',
        'location': 'г.Сочи, ул. Морская 2'
    }},
    '2': {'summary': 'Дубай', 'value': {
        'title': 'У фантана',
        'location': 'г.Дубай, ул. Шейха 1'
    }}
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepositories(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            '1': {
                'summary': 'Сочи',
                'value': {
                    'title': 'У моря',
                    'location': 'г.Сочи, ул. Морская 222'
                }}
        })
):

    async with async_session_maker() as session:
        await HotelsRepositories(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {'status': 'OK'}


@router.patch(
    '/{hotel_id}',
    summary='Патч данных отеля',
    description='Ручка обновления параметров отеля по отдельности. Доступны title, name'
)
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepositories(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepositories(session).delete(id=hotel_id)
        await session.commit()
    return {'status': 'OK'}
