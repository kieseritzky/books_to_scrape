import pytest
import unittest
from unittest.mock import AsyncMock, patch
from utils.retry import retry

@pytest.mark.asyncio
async def test_retry_succeeds_on_first_attempt():
    mock = AsyncMock(
        return_value = "Success"
    )
    result = await retry(mock)
    assert result == "Success"
    assert mock.await_count == 1

@pytest.mark.asyncio
async def test_retry_succeeds_on_second_attempt():
    mock = AsyncMock(
        side_effect = [RuntimeError, "Success"],
    )
    result = await retry(mock)
    assert result == "Success"
    assert mock.await_count == 2

@pytest.mark.asyncio
async def test_retry_succeeds_on_third_attempt():
    mock = AsyncMock(
        side_effect = [RuntimeError, RuntimeError, "Success"],
    )
    result = await retry(mock)
    assert result == "Success"
    assert mock.await_count == 3

@pytest.mark.asyncio
async def test_retry_first_sleep():
    mock = AsyncMock(
        side_effect = [
            RuntimeError,
            "Success"
        ]
    )

    with patch(
        "utils.retry.asyncio.sleep",
        new_callable = AsyncMock
    ) as mock_sleep:

        result = await retry(mock)

        assert result == "Success"
        assert mock.await_count == 2
        assert mock_sleep.await_count == 1

@pytest.mark.asyncio
async def test_retry_attempts():
    mock = AsyncMock(
        side_effect = RuntimeError()
    )

    with pytest.raises(RuntimeError):
        await retry(mock, retries=5)

    assert mock.await_count == 5