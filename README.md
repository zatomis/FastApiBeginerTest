docker network create myNetwork
 

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=user_pg \
    -e POSTGRES_PASSWORD=pass_pg \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16
 
docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4


docker run --name booking_back \
    -p 7777:8000 \
    --network=myNetwork \
    booking_image
 

docker build -t booking_image .