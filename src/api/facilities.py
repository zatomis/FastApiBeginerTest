from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.exceptions import ObjectNotFoundException, FacilityNotFoundHTTPException, IncorrectPasswordException
from src.schemas.facilities import FaclitiesAdd
from src.services.facilities import FacilityServiceLayer
from src.tasks.task import test_task
from redis.exceptions import ConnectionError


router = APIRouter(prefix="/facilities", tags=["Удобства 🚽"])


@router.get(
    "/", summary="Удобства", description="<H1>Получить данные об удобствах</H1>"
)
@cache(expire=10)
async def get_facilities(db: DBDep):
    # #пример на обычном Redis без плагинов
    # faclities_from_cashe = await redis_manager.get("facilities")
    # if not faclities_from_cashe:
    #     faclities = await db.facilities.get_all()
    #     #т.к Redis работает с строками - преобразуем
    #     #faclities-список PyDantic схем, то их преобразуем к списку словарей,
    #     #а потом в json
    #     faclities_schemas: list[dict] = [f.model_dump() for f in faclities]
    #     faclities_json = json.dumps(faclities_schemas)
    #     await redis_manager.set("facilities", faclities_json, 10)
    #     return faclities
    # else:
    #     faclities_dicts = json.loads(faclities_from_cashe)
    #     return faclities_dicts
    return await FacilityServiceLayer(db).get_facilities()


@router.post(
    "/",
    summary="Добавить удобства для номеров",
    description="<H1>Добавить удобства для номеров</H1>",
)

async def create_facility(db: DBDep, faclities_data: FaclitiesAdd = Body()):
    #проверка на дубликат
    faclities_data.title = faclities_data.title.strip()
    new_facilities = await db.facilities.get_filter(title=faclities_data.title)
    if not new_facilities:
        facilities = await db.facilities.add(faclities_data)
        await db.commit()
        test_task.delay()
        return {"status": "OK", "data": facilities}
    else:
        return {"status": "Данные не могут быть пустые"}


@router.delete(
    "/{facility_id}",
    summary="Удаление",
    description="<H1>Удалить данные об удобствах</H1>",
)
@cache(expire=30)
async def delete_facility(facility_id: int, db: DBDep):
    try:
        if await db.facilities.get_one(id=facility_id):
            await db.facilities.remove(id=facility_id)
            await db.commit()
            return {"status": "OK"}
    except ObjectNotFoundException:
        raise FacilityNotFoundHTTPException
    except ConnectionError:
        raise IncorrectPasswordException
