from fastapi import Query, APIRouter, Body

from sqlalchemy import insert

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])


hotels: list[dict[str, str | int]] = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get('')
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description='Айдишник'),
        title: str | None = Query(None, description='Название отеля'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page*(pagination.page-1):][:pagination.per_page]

    return hotels_

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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {'status': 'OK'}


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
