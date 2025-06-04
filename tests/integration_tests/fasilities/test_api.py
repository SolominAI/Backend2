async def test_get_facilities(ac):
    response = await ac.get('/facilities')
    print(f"{response.json()=}")
    assert response.status_code == 200


async def test_create_facility(ac):
    response = await ac.post(
        '/facilities',
        json={'title': 'Wi-Fi'}
    )
    print(f"{response.json()=}")
    assert response.status_code == 200
    assert response.json()['data']['title'] == 'Wi-Fi'