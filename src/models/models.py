from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import DateTime, Date


Base = declarative_base()


def get_current_time():
    return datetime.now(timezone.utc)


class SPIMEXTradingResults(Base):
    """
    Модель базы данных для хранения результатов торгов на SPIMEX.
    Атрибуты:
        id (int): Уникальный идентификатор записи.
        exchange_product_id (str): Код продукта.
        exchange_product_name (str): Наименование продукта.
        delivery_basis_name (str): Название базиса поставки.
        volume (float): Объём контрактов.
        total (float): Общая сумма.
        count (int): Количество контрактов.
        oil_id (str): Идентификатор нефти.
        delivery_basis_id (str): Идентификатор базиса поставки.
        delivery_type_id (str): Идентификатор типа поставки.
        date (Date): Дата торгов.
        created_on (datetime): Время создания записи.
        updated_on (datetime): Время последнего обновления записи.
    """

    __tablename__ = "spimex_trading_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    delivery_basis_name: Mapped[str]
    volume: Mapped[float]
    total: Mapped[float]
    count: Mapped[int]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_type_id: Mapped[str]
    date: Mapped[datetime] = mapped_column(Date)

    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_current_time
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_current_time, onupdate=get_current_time
    )
