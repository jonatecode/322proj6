import pytest
from flask import Flask
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_list_alll_json(client):
    response = client.get("/listAll/json")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert isinstance(data, list)
    if data:
        assert "open" in data[0]
        assert "close" in data[0]

def test_list_all_csv(client):
    response = client.get("/listAll/csv")
    assert response.status_code == 200
    assert response.content_type == 'text/csv'
    csv_data = response.data.decode('utf-8')
    assert 'open' in csv_data
    assert 'close' in csv_data

def test_list_open_only_json_top_3(client):
    response = client.get("/listOpenOnly/json?top=3")
    assert response.status == 200
    assert response.is_json
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) <= 3
    for item in data:
        assert isinstance(item, str)

def test_list_close_only_json_top_4(client):
    response = client.get("/listCloseOnly/json?top=4")
    assert response.status == 200
    assert response.is_json
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) <= 4
    for item in data:
        assert isinstance(item, str)

def test_list_close_only_csv_top_3(client):
    response = client.get("/listCloseOnly/csv?top=3")
    assert response.status_code == 200
    assert response.content_type == "text/csv"
    csv_data = response.data.decode('utf-8')
    lines = csv_data.strip().split("\n")
    assert len(lines) <= 5
    assert "close" in lines[0]