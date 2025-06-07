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
