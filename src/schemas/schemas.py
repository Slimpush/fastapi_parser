from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TradingFilters(BaseModel):
    oil_id: Optional[str] = None
    delivery_type_id: Optional[str] = None
    delivery_basis_id: Optional[str] = None


class TradingFiltersWithDates(TradingFilters):
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class TradingResultsSchema(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int = Field(ge=0)
    total: int = Field(ge=0)
    count: int = Field(ge=0)
    date: date
    created_on: datetime
    updated_on: datetime

    model_config = ConfigDict(from_attributes=True)


class LastTradingResultsDates(BaseModel):
    date: date


class TradingResultsList(BaseModel):
    trading_results: list[TradingResultsSchema]

    model_config = ConfigDict(from_attributes=True)
