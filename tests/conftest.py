from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy.orm import Session
import pytest, pytest_asyncio
from unittest.mock import AsyncMock
from database.test_connection import TestSessionLocal
from database.models import BasicData, AdvancedData
from api.main import app
from database.connection import get_db

@pytest.fixture
def client():
    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def basic_test_data():
    return{
        "title": "Test Data",
        "price": 28.009,
        "availability": "Available",
        "rating": 4,
    }

@pytest.fixture
def basic_product(basic_test_data):
    db = TestSessionLocal()

    try:
        product = BasicData(**basic_test_data)

        db.add(product)
        db.commit()
        db.refresh(product)

        return product
    finally:
        db.close()

    return product

@pytest.fixture
def advanced_test_data():
    return {
        "description": "klsdajfal;dsjfl;ajsd;klfjasd;fjlksdjfkdsjkldfjsldjflksajf;ladsf",
        "upc": "aedfdkje342kjk3kjk3k3k3j3k3j",
        "product_type": "Books",
        "price_excl_tax": 51.77,
        "price_incl_tax": 51.77,
        "tax": 0,
        "availability": "InStock(12 available)",
        "number_of_reviews": 4,
    }

@pytest.fixture
def advanced_prodcut(advanced_test_data):
    db = TestSessionLocal()
    try:
        product = AdvancedData(**advanced_test_data)

        db.add(product)
        db.commit()
        db.refresh(product)

    finally:
        db.close()

    return product 

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

