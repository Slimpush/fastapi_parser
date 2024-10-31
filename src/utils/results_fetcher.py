from typing import List, Optional

from filters.filters import get_filtered_query
from models.models import SPIMEXTradingResults
from schemas.schemas import TradingFilters, TradingResultsSchema
from utils.unit_of_work import UnitOfWork


async def fetch_trading_results(
    filters: TradingFilters,
    uow: UnitOfWork,
    use_dates: bool = False,
    limit_results: Optional[int] = None,
) -> List[TradingResultsSchema]:
    query = await get_filtered_query(filters, uow.session, use_dates=use_dates)

    if limit_results:
        query = query.order_by(SPIMEXTradingResults.date.desc()).limit(limit_results)

    result = await uow.session.execute(query)
    results = result.scalars().all()

    return [TradingResultsSchema.model_validate(r) for r in results]
