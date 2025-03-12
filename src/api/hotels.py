from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
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
    async with (async_session_maker() as session):
        repository = HotelsRepositories(session)
        result = await repository.add(hotel_data.model_dump())
        await session.commit()

        if result:
            hotel = result[0]
        else:
            return {"status": "error", "message": "Hotel not added"}

    return {"status": "OK", "data": hotel}


@router.put('/{hotel_id}')
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    hotel['title'] = hotel_data.title
    hotel['name'] = hotel_data.name
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


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}
