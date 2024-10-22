from fastapi import FastAPI
from .routers import router
from .settings import settings
from utils.cache import init_cache, reset_cache


app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def on_startup() -> None:
    await init_cache()
    if settings.redis_expire is None:
        settings.redis_expire = await reset_cache()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:main",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
