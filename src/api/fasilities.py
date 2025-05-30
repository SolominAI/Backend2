from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemas.fasilities import FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('')
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post('')
async def create_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(openapi_examples={
        '1': {'summary': 'Интернет', 'value': {'title': 'Интернет'}},
        '2': {'summary': 'Парковка', 'value': {'title': 'Бесплатная парковка'}}
    })
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
