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

docker run --name booking_celery_worker \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_app_task_instance worker -l INFO

docker run --name booking_celery_beat \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_app_task_instance worker -l INFO -B

[//]: # ( это локально)
docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=myNetwork \
    --rm -p 80:80 nginx 

[//]: # ( это на сервере + прокинуть папку с сертификатом)
docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --volume /etc/letsencrypt:/etc/letsencrypt \
    --volume /var/letsencrypt:/var/letsencrypt \
    --network=myNetwork \
    -d -p 80:80 -p 443:443 nginx 



docker build -t booking_image .