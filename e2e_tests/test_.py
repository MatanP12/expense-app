from requests import post,get,delete,put
import sys
import json
import pytest


@pytest.fixture()
def address():
    address = os.getenv("SERVER_ADDRESS", 'localhost')
    port=os.getenv("SERVER_PORT", "80")
    return f'http://{address}:{port}'

expenses = [
    {
        "product": "Tapuz",
        "price": 12
    },
    {
        "product" : "Avocado",
        "price" : 20
    }
]


def test_post_request_expense1(address):
    response = post(f'{address}/expenses', json=expenses[0])
    assert response.status_code == 201
    response_data = response.json()
    expenses[0]['id'] = response_data['id']
    assert response_data['product'] == expenses[0]['product']
    assert response_data['price'] == expenses[0]['price']

def test_post_request_expense2(address):
    response = post(f'{address}/expenses', json=expenses[1])
    assert response.status_code == 201
    response_data = response.json()
    expenses[1]['id'] = response_data['id']
    assert response_data['product'] == expenses[1]['product']
    assert response_data['price'] == expenses[1]['price']


def test_put_request(address):
    expenses[0]['price'] += 1.1
    response = put(f"{address}/expenses/{expenses[0]['id']}", json=expenses[0])
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['product'] == expenses[0]['product']
    assert response_data['price'] == expenses[0]['price']

def test_delete_request(address):
    response = delete(f"{address}/expenses/{expenses[1]['id']}")
    assert response.status_code == 200

def test_sanity(address):
    response= get(address)
    assert response.status_code == 200

def test_get_one(address):
    response = get(f"{address}/expenses/{expenses[0]['id']}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['product'] == expenses[0]['product']
    assert response_data['price'] == expenses[0]['price']

def test_get_all(address):
    response = get(f"{address}/expenses")
    assert response.status_code == 200
    res_list = list(response.json())
    assert len(res_list) == 1
    assert res_list[0]['product'] == expenses[0]['product']
    assert res_list[0]['price'] == expenses[0]['price']
