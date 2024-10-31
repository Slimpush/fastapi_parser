import pytest

from src.db.db_manager import insert_data

test_data = [
    (1, "Product1", 101, 201, "Basis1", 301, 1000.0, 100000.0, 10, "01.01.2023"),
    (2, "Product2", 102, 202, "Basis2", 302, 2000.0, 200000.0, 20, "02.01.2023"),
]


@pytest.mark.asyncio
async def test_insert_data_success(mocker):
    mock_session = mocker.AsyncMock()
    mocker.patch("src.db.db_manager.AsyncSessionFactory", return_value=mock_session)

    await insert_data(test_data)

    mock_session.__aenter__.return_value.add_all.assert_called_once()
    mock_session.__aenter__.return_value.commit.assert_called_once()


@pytest.mark.asyncio
async def test_insert_data_exception(mocker):
    mock_session = mocker.AsyncMock()
    mock_session.__aenter__.return_value.commit.side_effect = Exception(
        "Test exception"
    )
    mocker.patch("src.db.db_manager.AsyncSessionFactory", return_value=mock_session)

    await insert_data(test_data)

    mock_session.__aenter__.return_value.add_all.assert_called_once()
    mock_session.__aenter__.return_value.rollback.assert_called_once()
