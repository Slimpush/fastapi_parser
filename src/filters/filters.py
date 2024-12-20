from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.models import SPIMEXTradingResults
from schemas.schemas import TradingFilters


async def get_filtered_query(
    filters: TradingFilters, session: AsyncSession, use_dates: bool = False
):
    query = select(SPIMEXTradingResults)

    if filters.oil_id:
        query = query.filter(SPIMEXTradingResults.oil_id == filters.oil_id)
    if filters.delivery_type_id:
        query = query.filter(
            SPIMEXTradingResults.delivery_type_id == filters.delivery_type_id
        )
    if filters.delivery_basis_id:
        query = query.filter(
            SPIMEXTradingResults.delivery_basis_id == filters.delivery_basis_id
        )

    if use_dates and filters.start_date and filters.end_date:
        query = query.filter(
            filters.start_date <= SPIMEXTradingResults.date,
            SPIMEXTradingResults.date <= filters.end_date,
        )

    return query
