import pytest
import requests
import json

replace_me = 1

data = {
        "name": "pytest"
        }

def test_add_region(auth_as_admin):
    response = json.loads(requests.post(f"http://0.0.0.0:5000/regions/", data = json.dumps(data), cookies = {'token': auth_as_admin}).text)
    response.pop('id')

    assert response == data

def test_get_region(auth_as_admin):
    response = json.loads(requests.get(f"http://0.0.0.0:5000/regions/{replace_me}", cookies = {'token': auth_as_admin}).text)
    response.pop('id')

    assert response == data 

def test_put_region(auth_as_admin):
    data['name'] = 'pytest15'
    _ = json.loads((requests.put(f"http://0.0.0.0:5000/regions/{replace_me}", data = json.dumps(data), cookies = {'token': auth_as_admin})).text)

    response = json.loads(requests.get(f"http://0.0.0.0:5000/regions/{replace_me}", data = json.dumps(data), cookies = {'token': auth_as_admin}).text)
    response.pop('id')

    assert response == data


@pytest.mark.xfail()
def test_delete_region(auth_as_admin):
    response = requests.delete(f"http://0.0.0.0:5000/regions/{replace_me}", cookies = {'token': auth_as_admin})
    
    assert response == data
