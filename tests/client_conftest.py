import pytest


@pytest.fixture
def client_request(db, client):
    return client