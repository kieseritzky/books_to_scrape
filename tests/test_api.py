from database.test_connection import test_engine
from api.main import app
from database.connection import Base
from starlette.testclient import TestClient

Base.metadata.create_all(bind=test_engine)


def test_book_not_found(client):
    response = client.get("/advanced/abc")

    assert response.status_code == 422

def test_get_existing_book(client, basic_product):
    response = client.get("/basic/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Test Data"

def test_get_non_existing_book(client):
    response = client.get("/advanced/9999")

    assert response.status_code == 404

def test_advanced(client, advanced_prodcut):
    response = client.get("/advanced/1")

    assert response.status_code == 200
    assert response.json()["tax"] == 0

def test_get_all_basic_data(client):
    response = client.get("/basic")

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert any(item["title"] == "Test Data" for item in data)

def test_get_basic_data_limit(client):
    response = client.get("/basic")

    assert response.status_code == 200
    assert len(response.json()) <= 10