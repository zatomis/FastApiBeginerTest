import shutil
from fastapi import APIRouter, UploadFile

from src.tasks.task import resize_image

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("")
def upload_image(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as image_new_file:
        shutil.copyfileobj(file.file, image_new_file)

    resize_image(image_path)