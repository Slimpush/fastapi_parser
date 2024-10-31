from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers import router
from api.settings import settings
from utils.cache import init_cache, reset_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_cache()
    if settings.redis_expire is None:
        settings.redis_expire = await reset_cache()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:main",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
