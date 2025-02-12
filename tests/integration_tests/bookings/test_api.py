import pytest

@pytest.mark.parametrize("room_id, date_from, date_to, status_code",[
    (1, "2024-02-01", "2024-02-11", 200),
    (1, "2024-02-01", "2024-02-11", 200),
    (1, "2024-02-01", "2024-02-11", 200),
    (1, "2024-02-01", "2024-02-11", 200),
    (1, "2024-02-01", "2024-02-11", 200),
    (1, "2024-02-01", "2024-02-11", 500),
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
