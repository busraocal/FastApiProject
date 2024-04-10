import pytest
import requests


@pytest.fixture
def test_device_data():
    return {
        "name": "Test Device"
    }


def test_create_device(test_device_data):
    response = requests.post("http://127.0.0.1:8000/insert_device", json=test_device_data)
    assert response.status_code == 200
    assert response.json() == {'message': 'Successfull'}


def test_integration():
    response = requests.get("http://127.0.0.1:8000/all_device_list/")
    assert response.status_code == 200
