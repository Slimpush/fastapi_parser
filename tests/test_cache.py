from datetime import datetime, timedelta

import pytest

from src.utils.cache import get_redis_connection, reset_cache


@pytest.mark.asyncio
async def test_redis_connection(mock_redis_connection):
    await get_redis_connection()
    mock_redis_connection.from_url.assert_called_once_with(
        "redis://redis:6379", decode_responses=True
    )


@pytest.mark.asyncio
async def test_reset_cache():
    now = datetime.now()
    seconds_until_reset = reset_cache()

    next_reset_time = now.replace(hour=14, minute=11, second=0, microsecond=0)
    if now >= next_reset_time:
        next_reset_time += timedelta(days=1)

    expected_seconds_until_reset = int((next_reset_time - now).total_seconds())

    assert isinstance(seconds_until_reset, int)
    assert seconds_until_reset == expected_seconds_until_reset
    assert 0 < seconds_until_reset <= 86400
