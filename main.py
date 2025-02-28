from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels: list[dict[str, str | int]] = [
    {"id": 1, "title": "Sochi", 'name': 'Sochi5787'},
    {"id": 2, "title": "Dubai", 'name': 'Dubai4568'},
]


@app.get('/hotels')
def get_hotels(
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

    return hotels_


@app.post('/hotels')
def create_hotel(
        title: str = Body(embed=True, description=''),
):
    global hotels
    hotels.append({
        'id': int(hotels[-1]['id']) + 1,
        'title': title
    })


@app.put('/hotels/{hotel_id}')
def edit_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body(),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    hotel['title'] = title
    hotel['name'] = name
    return {'status': 'OK'}


@app.patch(
    '/hotels/{hotel_id}',
    summary='Патч данных отеля',
    description='Ручка обновления параметров отеля по отдельности. Доступны title, name'
)
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    if title is not None and title != "string":
        hotel['title'] = title
    if name is not None and name != "string":
        hotel['name'] = name
    return {'status': 'OK'}git 


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
