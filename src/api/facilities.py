from datetime import date
from fastapi import APIRouter, Body, Query
from src.api.dependencies import DBDep
from src.schemas.facilities import FaclitiesAdd
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix='/facilities', tags=["Удобства 🚽"])


@router.get("/",
            summary="Удобства",
            description="<H1>Получить данные об удобствах</H1>")
async def get_facilities(db: DBDep):

    faclities = await db.facilities.get_all()
    return {"status": "OK", "data": faclities}


@router.post("/",
           summary="Добавить удобства для номеров",
           description="<H1>Добавить удобства для номеров</H1>")
async def create_room(db: DBDep,
                      faclities_data: FaclitiesAdd = Body()):
    faclities = await db.facilities.add(faclities_data)
    await db.commit()
    return {"status": "OK", "data": faclities}
