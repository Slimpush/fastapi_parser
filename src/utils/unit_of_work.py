from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_manager import get_session


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.transaction = await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.transaction.rollback()
        else:
            await self.transaction.commit()

    async def rollback(self):
        await self.transaction.rollback()


async def get_uow(session: AsyncSession = Depends(get_session)) -> UnitOfWork:
    async with UnitOfWork(session) as uow:
        yield uow
