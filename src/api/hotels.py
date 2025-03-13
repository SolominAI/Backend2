from fastapi import Query, APIRouter, Body, HTTPException
from sqlalchemy.exc import MultipleResultsFound

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import Hotel, HotelPATCH

from src.repositories.hotels import HotelsRepositories

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


@router.post('')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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


@router.put('')
async def edit_hotel(
    hotel_id: int | None = Query(None),
    title: str | None = Query(None),
    location: str | None = Query(None),
    hotel_data: Hotel = Body(
        openapi_examples={
            '1': {
                'summary': 'Сочи',
                'value': {
                    'title': 'У моря',
                    'location': 'г.Сочи, ул. Морская 222'
                }}
        })):

    filter_params = {}
    if hotel_id:
        filter_params['id'] = hotel_id
    if title:
        filter_params['title'] = title
    if location:
        filter_params['location'] = location

    async with async_session_maker() as session:
        try:
            hotel = await HotelsRepositories(session).get_one_or_none(**filter_params)
        except MultipleResultsFound:
            raise HTTPException(status_code=400, detail='Найдено более одного отеля')

        if hotel is None:
            raise HTTPException(status_code=404, detail='Отель не найден')

        await HotelsRepositories(session).edit(hotel_data, **filter_params)
        await session.commit()

    return {'status': 'OK'}


@router.patch(
    '/{hotel_id}',
    summary='Патч данных отеля',
    description='Ручка обновления параметров отеля по отдельности. Доступны title, name'
)
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    if hotel_data.title is not None and hotel_data.title != "string":
        hotel['title'] = hotel_data.title
    if hotel_data.name is not None and hotel_data.name != "string":
        hotel['name'] = hotel_data.name
    return {'status': 'OK'}


@router.delete('')
async def delete_hotel(
    hotel_id: int | None = Query(None),
    title: str | None = Query(None),
    location: str | None = Query(None)
):

    filter_params = {}
    if hotel_id:
        filter_params['id'] = hotel_id
    if title:
        filter_params['title'] = title
    if location:
        filter_params['location'] = location

    async with async_session_maker() as session:
        try:
            hotel = await HotelsRepositories(session).get_one_or_none(**filter_params)
        except MultipleResultsFound:
            raise HTTPException(status_code=400, detail='Найдено более одного отеля')

        if hotel is None:
            raise HTTPException(status_code=404, detail='Отель не найден')

        await HotelsRepositories(session).delete(**filter_params)
        await session.commit()
    return {'status': 'OK'}
