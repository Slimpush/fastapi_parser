from datetime import datetime
from typing import AsyncGenerator

from .config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from models.models import Base, SPIMEXTradingResults
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, echo=True)

AsyncSessionFactory = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data(data_list: list[tuple]) -> None:
    async with AsyncSessionFactory() as session:
        try:
            results = [
                SPIMEXTradingResults(
                    exchange_product_id=data[0],
                    exchange_product_name=data[1],
                    oil_id=data[2],
                    delivery_basis_id=data[3],
                    delivery_basis_name=data[4],
                    delivery_type_id=data[5],
                    volume=data[6],
                    total=data[7],
                    count=data[8],
                    date=datetime.strptime(data[9], "%d.%m.%Y"),
                )
                for data in data_list
            ]
            session.add_all(results)
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при вставке данных: {e}")
