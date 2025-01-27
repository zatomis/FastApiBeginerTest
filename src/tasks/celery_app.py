from celery import Celery
from celery.bin.celery import celery

from src.config import settings


celery_app_task_instance = Celery(
    name= "tasks", #название
    broker= settings.REDIS_URL, #редис для работы
    include=[ #где будут храниться файлы с задачами
        "src.tasks.task",
    ],

)

# запуск Celery
# celery --app=src.tasks.celery_app:celery_app_task_instance worker -l INFO