from sqlalchemy import select, func
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM


def rooms_ids_for_booking(date_from, date_to, hotel_id: int | None = None):
    """
        получить id - готовые для бронирования, это сам запрос

    with rooms_count as (
    select room_id, count(*) as rooms_booked from bookings
    where date_from <= '2024-12-18' and date_to >= '2024-10-18'
    group by room_id
    ),
    rooms_left_not_null_table as (
    select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left from rooms
    left join rooms_count on rooms.id = rooms_count.room_id
    )
    select * from rooms_left_not_null_table where rooms_left > 0
    ------------------------------------------------------------------------
    """
    # 1я часть запроса
    # with rooms_count as (
    #         select room_id, count( *) as rooms_booked from bookings
    # where date_from <= '2024-12-18' and date_to >= '2024-10-18'
    # group by room_id),
    query_rooms_count = (
        select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsORM)
        .filter(
            BookingsORM.date_from <= date_to, BookingsORM.date_to >= date_from
        )
        .group_by(BookingsORM.room_id)
        .cte(name="query_rooms_count")
    )

    # 2я часть запроса
    # rooms_left_not_null_table as (
    # select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left from rooms
    # left join rooms_count on rooms.id = rooms_count.room_id)

    rooms_left_not_null_table = (
        select(
            RoomsORM.id.label("room_id"),
            (
                RoomsORM.quantity
                - func.coalesce(query_rooms_count.c.rooms_booked, 0)
            ).label("rooms_left"),
        )
        .select_from(RoomsORM)
        .outerjoin(
            query_rooms_count, RoomsORM.id == query_rooms_count.c.room_id
        )
        .cte(name="rooms_left_not_null_table")
    )

    # 3я часть
    # select * from rooms_left_not_null_table where rooms_left > 0
    rooms_ids_in_hotel = select(RoomsORM.id).select_from(RoomsORM)

    if hotel_id is not None:
        rooms_ids_in_hotel = rooms_ids_in_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_in_hotel = rooms_ids_in_hotel.subquery(name="rooms_ids_in_hotel")

    # получим только те номера, которые не забронированы и относятся к конкретному отелю
    sql_query_rooms_id_to_get = (
        select(rooms_left_not_null_table.c.room_id)
        .select_from(rooms_left_not_null_table)
        .filter(
            rooms_left_not_null_table.c.rooms_left > 0,
            rooms_left_not_null_table.c.room_id.in_(rooms_ids_in_hotel),
        )
    )

    return sql_query_rooms_id_to_get
