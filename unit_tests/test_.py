import pytest
from requests import get
import os

@pytest.fixture()
def address():
    address = os.getenv("SERVER_ADDRESS", 'localhost')
    port=os.getenv("SERVER_PORT", "5000")
    return f'http://{address}:{port}'


def test_sanity(address):
    response= get(address)
    assert response.status_code == 200
