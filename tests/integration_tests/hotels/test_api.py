from pprint import pprint


async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2024-08-01",
            "date_to": "2024-08-20",
        }
    )
    pprint(f"{response=}")

    assert response.status_code == 200
