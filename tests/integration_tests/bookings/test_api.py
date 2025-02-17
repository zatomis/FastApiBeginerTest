from pprint import pprint

import pytest

from src.database import new_async_session_maker_null_pool
from src.utils.db_manager import DBManager


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
    # room_id = (await db.rooms.get_all())[0].id
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



@pytest.fixture(scope="session")
async def clear_DB_bookings(check_test_mode):
    print("ФИКСТУРА на очистку бронирований")
    async with DBManager(session_factory=new_async_session_maker_null_pool) as db_:
        await db_.bookings.remove()
        await db_.commit()



@pytest.mark.parametrize("room_id, date_from, date_to, status_code",[
    (1, "2024-02-01", "2024-02-03", 1),
    (1, "2024-02-01", "2024-02-03", 2),
    (1, "2024-02-01", "2024-02-03", 3),])
async def test_add_and_get_my_bookings(
    clear_DB_bookings, db,
    room_id, date_from, date_to, status_code,
    autheticated_user_ac
    ):
    user = (await db.users.get_all())[0]

    response = await autheticated_user_ac.get(
        "/bookings/me",
        params={
            "user_id": user.id,
        }
    )
    pprint(f"{response.json()=}")