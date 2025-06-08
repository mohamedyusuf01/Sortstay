import importlib
import sys
from pathlib import Path

import pytest

# Allow importing the backend package
sys.path.append(str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def app():
    module = importlib.import_module('backend.app')
    module.app.config.update({'TESTING': True})
    return module.app


@pytest.fixture
def client(app):
    return app.test_client()


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'ok'}


def test_availability_and_booking(client):
    # Add available room
    res = client.post('/availability', json={'hotel': 'Hotel', 'room_id': '1'})
    assert res.status_code == 201

    # List rooms should show the added room
    res = client.get('/rooms')
    assert res.status_code == 200
    data = res.get_json()
    assert {'hotel': 'Hotel', 'room_id': '1'} in data['rooms']

    # Book the room
    res = client.post('/book', json={'room_id': '1'})
    assert res.status_code == 200
    assert res.get_json()['status'] == 'booked'

    # Room should no longer be listed
    res = client.get('/rooms')
    assert {'hotel': 'Hotel', 'room_id': '1'} not in res.get_json()['rooms']
