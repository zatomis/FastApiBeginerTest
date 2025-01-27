from time import sleep
from src.tasks.celery_app import celery_app_task_instance


@celery_app_task_instance.task
def test_task():
    sleep(15)
    print("Задача выполнена")
