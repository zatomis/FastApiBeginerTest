import pytest
from tests.conftest import get_db_null_pull


@pytest.mark.parametrize("room_id, date_from, date_to, status_code",[
    (1, "2024-02-01", "2024-02-11", 200),
    (1, "2024-02-01", "2024-02-11", 200),
    (2, "2024-02-01", "2024-02-11", 200),
    (1, "2024-02-01", "2024-02-11", 200),
    (1, "2024-02-01", "2024-02-11", 200),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, autheticated_user_ac):
    response = await autheticated_user_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def clear_DB_bookings(check_test_mode):
    # print("ФИКСТУРА на очистку бронирований")
    async for db_ in get_db_null_pull():
        await db_.bookings.remove()
        await db_.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, rooms_booked_number",[
    (12, "2024-02-01", "2024-02-03", 1),
    (12, "2024-02-01", "2024-02-03", 2),
    (12, "2024-02-01", "2024-02-03", 3),])
async def test_add_and_get_my_bookings(
    room_id, date_from, date_to, rooms_booked_number,
    autheticated_user_ac, clear_DB_bookings,
    ):

    response = await autheticated_user_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == 200

    response_my_bookings = await autheticated_user_ac.get(
        "/bookings/me"
    )
    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == rooms_booked_number
