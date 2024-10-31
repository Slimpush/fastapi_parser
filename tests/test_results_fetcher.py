import pytest

from src.filters.filters import get_filtered_query
from src.schemas.schemas import TradingFilters


@pytest.mark.asyncio
async def test_get_filtered_query(get_test_session):
    async with get_test_session as session:
        filters = TradingFilters(oil_id="oil1", delivery_basis_id="basis1")
        query = await get_filtered_query(filters, session)

        assert query.compile().params["oil_id_1"] == "oil1"
        assert query.compile().params["delivery_basis_id_1"] == "basis1"
