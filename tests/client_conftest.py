import pytest

from django.test.client import Client


@pytest.fixture
def client_request(db, client) -> Client:
    return client
