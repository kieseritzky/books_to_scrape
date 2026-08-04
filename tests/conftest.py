import pytest, pytest_asyncio
from unittest.mock import AsyncMock

@pytest.fixture
def expected_book():
    return {
        "title": "Python book",
        "author": "John Smith",
        "price": "20.99",
        "availabilty": "yes",
        "rating": "5",
    }

@pytest_asyncio.fixture
async def mock_page():
    page = AsyncMock()
    return page

@pytest_asyncio.fixture
async def mock_context():
    context = AsyncMock()
    return context

@pytest_asyncio.fixture
async def mock_progress():
    progress = AsyncMock()
    return progress

@pytest_asyncio.fixture
async def mock_parser(expected_book):
    mock_parser = AsyncMock(return_value=expected_book)
    return mock_parser

