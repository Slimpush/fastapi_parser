from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.future import select

from models.models import SPIMEXTradingResults
from schemas.schemas import (
    LastTradingResultsDates,
    TradingFilters,
    TradingFiltersWithDates,
    TradingResultsSchema,
)
from utils.cache import reset_cache
from utils.results_fetcher import fetch_trading_results
from utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter()


@router.get("/get_dynamics/", response_model=List[TradingResultsSchema])
@cache(expire=reset_cache())
async def get_dynamics(
    filters: TradingFiltersWithDates = Depends(), uow: UnitOfWork = Depends(get_uow)
) -> List[TradingResultsSchema]:
    return await fetch_trading_results(filters, uow, use_dates=True)


@router.get("/get_last_trading_dates/", response_model=List[LastTradingResultsDates])
@cache(expire=reset_cache())
async def get_last_trading_dates(
    limit: int = 5, uow: UnitOfWork = Depends(get_uow)
) -> List[LastTradingResultsDates]:
    query = (
        select(SPIMEXTradingResults.date)
        .distinct()
        .order_by(SPIMEXTradingResults.date.desc())
        .limit(limit)
    )
    result = await uow.session.execute(query)
    dates = result.scalars().all()
    return [{"date": d} for d in dates]


@router.get("/trading_results/", response_model=List[TradingResultsSchema])
@cache(expire=reset_cache())
async def get_trading_results(
    filters: TradingFilters = Depends(), uow: UnitOfWork = Depends(get_uow)
) -> List[TradingResultsSchema]:
    return await fetch_trading_results(filters, uow, use_dates=False, limit_results=10)
