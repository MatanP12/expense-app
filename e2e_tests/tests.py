from requests import post,get,delete,put
import sys
import json
URL = f'http://{sys.argv[1] if sys.argv[1] else "localhost:5000"}' 


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

def post_request(index):
    response = post(f'{URL}/expenses', json=expenses[index])
    assert response.status_code == 201
    response_data = response.json()
    expenses[index]['id'] = response_data['_id']
    assert response_data['product'] == expenses[index]['product']
    assert response_data['price'] == expenses[index]['price']

def put_request(index):
    expenses[index]['price'] += 1.1
    response = put(f"{URL}/expenses/{expenses[index]['id']}", json=expenses[index])
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['product'] == expenses[index]['product']
    assert response_data['price'] == expenses[index]['price']

def delete_request(index):
    response = delete(f"{URL}/expenses/{expenses[index]['id']}")
    assert response.status_code == 200

def sanity():
    response= get(URL)
    assert response.status_code == 200

def get_one(index):
    response = get(f"{URL}/expenses/{expenses[index]['id']}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['product'] == expenses[index]['product']
    assert response_data['price'] == expenses[index]['price']

def get_all():
    response = get(f"{URL}/expenses")
    assert response.status_code == 200
    res_list = list(response.json())
    assert len(res_list) == 1
    assert res_list[0]['product'] == expenses[0]['product']
    assert res_list[0]['price'] == expenses[0]['price']

if __name__ == "__main__":
    sanity()
    post_request(0)
    post_request(1)
    put_request(0)
    get_one(0)
    delete_request(1)
    get_all()
    print("Passed all the tests!")

