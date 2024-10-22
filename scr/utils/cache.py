from fastapi_cache import FastAPICache
from redis.asyncio import Redis
from datetime import datetime, timedelta
from fastapi_cache.backends.redis import RedisBackend


async def get_redis_connection() -> Redis:
    return Redis.from_url("redis://redis:6379", decode_responses=True)


async def init_cache() -> None:
    redis = await get_redis_connection()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


def reset_cache() -> int:
    now = datetime.now()
    next_reset = now.replace(hour=14, minute=11, second=0, microsecond=0)
    if now >= next_reset:
        next_reset += timedelta(days=1)
    expire_seconds = (next_reset - now).total_seconds()
    return int(expire_seconds)
