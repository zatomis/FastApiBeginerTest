import logging
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn
from contextlib import asynccontextmanager
import sys
from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# это для того, чтобы питон верно нашел и запустил основной файл !!!
# добавить эту папку в пути-чтобы интерпритатор работал
sys.path.append(str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.INFO)

from src.setup import redis_manager # noqa : E402
from src.api.auth import router as router_auth # noqa : E402
from src.api.hotels import router as router_hotels # noqa : E402
from src.api.rooms import router as router_rooms # noqa : E402
from src.api.bookings import router as router_bookings # noqa : E402
from src.api.facilities import router as router_facilities # noqa : E402
from src.api.images import router as router_images # noqa : E402

@asynccontextmanager
async def lifespan(app: FastAPI):
    # тут при старте
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    # тут при закрытии
    await redis_manager.close()


# lifespan это функция - которая стартует и закрывается вместе с FA
app = FastAPI(docs_url=None, lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


@app.get("/")
def func():
    return "Hello World!!!!!!!!!!"


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
