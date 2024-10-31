import asyncio
import os
from io import BytesIO

import pandas as pd
import pytest
from dotenv import load_dotenv
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.db.db_manager import AsyncSessionFactory
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(".test.env")


DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")

MOCK_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


mock_engine = create_async_engine(MOCK_DATABASE_URL, echo=True)
MockAsyncSessionFactory = sessionmaker(
    bind=mock_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def get_test_session():
    async with AsyncSessionFactory() as session:
        yield session


@pytest.fixture(scope="function")
def mock_redis_connection(mocker):
    mock_redis = mocker.patch("src.utils.cache.Redis")
    mock_redis.from_url = mocker.AsyncMock()
    return mock_redis


@pytest.fixture(scope="function", autouse=True)
def init_cache(mock_redis_connection):
    FastAPICache.init(RedisBackend(mock_redis_connection), prefix="test-cache")


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
def sample_xls_content():
    data = {
        "B": ["ABCD123", "EFGH456", "IJKL789"],
        "C": ["Product A", "Product B", "Product C"],
        "D": ["Basis A", "Basis B", "Basis C"],
        "E": [100, 0, 200],
        "F": [10000, 5000, 20000],
        "O": [10, 0, 15],
    }
    df = pd.DataFrame(data)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)
    return buffer.getvalue()


@pytest.fixture(scope="function")
def sample_date():
    return "01.01.2024"
