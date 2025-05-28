import json

from fastapi import APIRouter, Body
from src.init import redis_manager
from src.schemas.fasilities import FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('')
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    print(f"{facilities_from_cache=}")
    if not facilities_from_cache:
        print(f"Иду в базу данных")
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set('facilities', facilities_json, 10)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts


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
