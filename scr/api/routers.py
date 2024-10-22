from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from filters.filters import get_filtered_query
from models.models import SPIMEXTradingResults
from db.db_manager import get_session
from schemas.schemas import (
    LastTradingResultsDates,
    TradingFilters,
    TradingResultsSchema,
)
from sqlalchemy.future import select
from utils.cache import reset_cache


router = APIRouter()


async def fetch_trading_results(
    filters: TradingFilters,
    session: AsyncSession,
    use_dates: bool = False,
    limit_results: Optional[int] = None
) -> List[TradingResultsSchema]:
    query = await get_filtered_query(filters, session, use_dates=use_dates)

    if limit_results:
        query = query.order_by(
            SPIMEXTradingResults.date.desc()).limit(limit_results)

    result = await session.execute(query)
    results = result.scalars().all()

    return [TradingResultsSchema.model_validate(r) for r in results]


@router.get("/get_dynamics/", response_model=List[TradingResultsSchema])
@cache(expire=reset_cache())
async def get_dynamics(
    filters: TradingFilters = Depends(),
    session: AsyncSession = Depends(get_session)
) -> List[TradingResultsSchema]:
    return await fetch_trading_results(filters, session, use_dates=True)


@router.get(
        "/get_last_trading_dates/",
        response_model=List[LastTradingResultsDates]
    )
@cache(expire=reset_cache())
async def get_last_trading_dates(
    limit: int = 5,
    session: AsyncSession = Depends(get_session)
) -> List[LastTradingResultsDates]:
    query = select(SPIMEXTradingResults.date).distinct().order_by(
        SPIMEXTradingResults.date.desc()).limit(limit)
    result = await session.execute(query)
    dates = result.scalars().all()
    return [{"date": d} for d in dates]


@router.get(
    "/trading_results/",
    response_model=List[TradingResultsSchema]
)
@cache(expire=reset_cache())
async def get_trading_results(
    filters: TradingFilters = Depends(),
    session: AsyncSession = Depends(get_session)
) -> List[TradingResultsSchema]:
    return await fetch_trading_results(
        filters,
        session,
        use_dates=False,
        limit_results=10
    )
