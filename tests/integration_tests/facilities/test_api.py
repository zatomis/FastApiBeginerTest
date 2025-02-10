from pprint import pprint


async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities/",
    )
    pprint(f"{response=}")
    assert response.status_code == 200


async def test_add_facilities(ac):
    response = await ac.post(
        "/facilities",
        params={
            "title": "Личный водитель",
        }
    )
    pprint(f"{response=}")
