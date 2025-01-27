import asyncio
import os
from time import sleep

from PIL import Image

from src.database import new_async_session_maker
from src.tasks.celery_app import celery_app_task_instance
from src.utils.db_manager import DBManager


@celery_app_task_instance.task
def test_task():
    sleep(15)
    print("Задача выполнена")


@celery_app_task_instance.task
def resize_image(image_path: str):
    sizes = [1000, 500, 200]
    output_folder = 'src/static/images'
    # Открываем изображение
    img = Image.open(image_path)
    # Получаем имя файла и его расширение
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    # Проходим по каждому размеру
    for size in sizes:
        # Сжимаем изображение
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)
        # Формируем имя нового файла
        new_file_name = f"{name}_{size}px{ext}"
        # Полный путь для сохранения
        output_path = os.path.join(output_folder, new_file_name)
        # Сохраняем изображение
        img_resized.save(output_path)
    print(f"Изображение сохранено в следующих размерах: {sizes} в папке {output_folder}")


async def get_bookings_with_today_checkin_helper():
    print("Я ЗАПУСКАЮСЬ")
    async with DBManager(session_factory=new_async_session_maker) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_app_task_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())