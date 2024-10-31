from datetime import datetime

from src.models.models import SPIMEXTradingResults


def test_spimex_trading_results_model():
    instance = SPIMEXTradingResults(
        exchange_product_id="prod1",
        exchange_product_name="Product Name",
        delivery_basis_name="Basis Name",
        volume=100.0,
        total=200.0,
        count=5,
        oil_id="oil1",
        delivery_basis_id="basis1",
        delivery_type_id="type1",
        date=datetime.strptime("01.01.2023", "%d.%m.%Y"),
    )

    assert instance.exchange_product_id == "prod1"
    assert instance.exchange_product_name == "Product Name"
    assert instance.delivery_basis_name == "Basis Name"
    assert instance.volume == 100.0
    assert instance.total == 200.0
    assert instance.count == 5
    assert instance.oil_id == "oil1"
    assert instance.delivery_basis_id == "basis1"
    assert instance.delivery_type_id == "type1"
    assert instance.date == datetime.strptime("01.01.2023", "%d.%m.%Y")
