from celery import Celery
from src.config import settings


celery_app_task_instance = Celery(
    name="tasks",  # название
    broker=settings.REDIS_URL,  # редис для работы
    include=[  # где будут храниться файлы с задачами
        "src.tasks.task",
    ],
)

celery_app_task_instance.conf.beat_schedule = {
    "Schedure_tasks": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}

# запуск Celery -B это запуск задач по рассписанию
# celery --app=src.tasks.celery_app:celery_app_task_instance worker -l INFO -B
