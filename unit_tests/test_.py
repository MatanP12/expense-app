import pytest
from requests import get


@pytest.fixture()
def address():
    return 'http://server:5000'


def test_sanity(address):
    response= get(address)
    assert response.status_code == 200
