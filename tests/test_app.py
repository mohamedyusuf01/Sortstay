import importlib
import sys
from pathlib import Path

import pytest

# Allow importing the backend package
sys.path.append(str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def app():
    db_path = Path('sortstay.db')
    if db_path.exists():
        db_path.unlink()
    if 'backend.app' in sys.modules:
        del sys.modules['backend.app']
    module = importlib.import_module('backend.app')
    module.app.config.update({'TESTING': True})
    with module.app.app_context():
        module.db.drop_all()
        module.db.create_all()
    return module.app


@pytest.fixture
def client(app):
    return app.test_client()


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'ok'}


def register_and_login(client, username, role):
    res = client.post('/register', json={
        'username': username,
        'password': 'pass',
        'role': role,
    })
    assert res.status_code == 200
    res = client.post('/login', json={'username': username, 'password': 'pass'})
    assert res.status_code == 200
    return res.get_json()['token']


def test_availability_and_booking(client):
    hotel_token = register_and_login(client, 'hotel1', 'hotel')
    council_token = register_and_login(client, 'council1', 'council')

    # Add available room
    res = client.post(
        '/availability',
        json={'room_id': '1', 'price': 80.0},
        headers={'Authorization': hotel_token},
    )
    assert res.status_code == 201

    # List rooms should show the added room
    res = client.get('/rooms', headers={'Authorization': council_token})
    assert res.status_code == 200
    data = res.get_json()
    assert any(r['room_id'] == '1' and r['hotel'] == 'hotel1' for r in data['rooms'])

    # Book the room
    res = client.post(
        '/book',
        json={'room_id': '1', 'nights': 2},
        headers={'Authorization': council_token},
    )
    assert res.status_code == 200
    assert res.get_json()['status'] == 'booked'

    # Room should no longer be listed
    res = client.get('/rooms', headers={'Authorization': council_token})
    assert not any(r['room_id'] == '1' for r in res.get_json()['rooms'])

