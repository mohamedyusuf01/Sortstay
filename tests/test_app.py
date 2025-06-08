import importlib
import sys
from pathlib import Path

import pytest

# Allow importing the backend package
sys.path.append(str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def app():
    module = importlib.import_module('backend.app')
    # Reload module to reset global state between tests
    module = importlib.reload(module)
    module.app.config.update({'TESTING': True})
    return module.app


@pytest.fixture
def client(app):
    return app.test_client()


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'ok'}


def create_council(client, name, budget):
    resp = client.post('/councils', json={'name': name, 'budget': budget})
    assert resp.status_code == 201
    return resp.get_json()['id']


def create_booking(client, council_id, hotel, cost):
    return client.post('/bookings', json={'council_id': council_id, 'hotel': hotel, 'cost': cost})


def test_booking_reduces_budget(client):
    cid = create_council(client, 'Test Council', 200)
    resp = create_booking(client, cid, 'Hotel A', 50)
    assert resp.status_code == 201
    budget_resp = client.get(f'/councils/{cid}/budget')
    data = budget_resp.get_json()
    assert data['budget_remaining'] == 150
    assert len(data['bookings']) == 1


def test_booking_insufficient_funds(client):
    cid = create_council(client, 'Low Budget', 50)
    resp = create_booking(client, cid, 'Hotel A', 100)
    assert resp.status_code == 400
    budget_resp = client.get(f'/councils/{cid}/budget')
    data = budget_resp.get_json()
    assert data['budget_remaining'] == 50
    assert data['bookings'] == []
