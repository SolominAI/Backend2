from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Местоположения и адрес"),
    date_from: date = Query(example="2025-05-01"),
    date_to: date = Query(example="2025-05-15"),
):
    return await HotelService(db).get_filtred_by_time(
        pagination,
        title,
        location,
        date_from,
        date_to)


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "У моря", "location": "г.Сочи, ул. Морская 2"},
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "У фантана", "location": "г.Дубай, ул. Шейха 1"},
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "У моря", "location": "г.Сочи, ул. Морская 222"},
            }
        }),
):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Патч данных отеля",
    description="Ручка обновления параметров отеля по отдельности. Доступны title, name",
)
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
