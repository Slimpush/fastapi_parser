import pytest

from src.db.db_manager import get_session
from src.main import app
from tests.conftest import get_test_session

app.dependency_overrides[get_session] = get_test_session


@pytest.mark.asyncio
async def test_get_dynamics(client):
    response = await client.get("/get_dynamics/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_last_trading_dates(client):
    response = await client.get("/get_last_trading_dates/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all("date" in item for item in response.json())


@pytest.mark.asyncio
async def test_get_trading_results(client):
    response = await client.get("/trading_results/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
