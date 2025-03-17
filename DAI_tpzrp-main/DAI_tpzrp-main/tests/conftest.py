import pytest
import requests
import json

@pytest.fixture()
def sign_up_as_admin(scope = 'module'):
    data = {
        "role": "admin",
        "email": "admin@mail.ru",
        "password": "admin"
        }

    response = requests.post(f"http://0.0.0.0:5002/sign_up/", data = json.dumps(data))


@pytest.fixture()
def auth_as_admin(sign_up_as_admin, scope = 'module'):
    data = {
        "email": "admin@mail.ru",
        "password": "admin"
        }

    response = requests.post(f"http://0.0.0.0:5002/sign_in/", data = json.dumps(data))
    response_json = json.loads(response.text)

    return response_json['access_token']


@pytest.fixture()
def sign_up_as_director(scope = 'module'):
    data = {
        "role": "director",
        "email": "director@mail.ru",
        "password": "director"
        }

    response = requests.post(f"http://0.0.0.0:5002/sign_up/", data = json.dumps(data))


@pytest.fixture()
def auth_as_director(sign_up_as_director, scope = 'module'):
    data = {
        "email": "director@mail.ru",
        "password": "director"
        }

    response = requests.post(f"http://0.0.0.0:5002/sign_in/", data = json.dumps(data))
    response_json = json.loads(response.text)

    return response_json['access_token']


@pytest.fixture()
def sign_up_as_doctor(scope = 'module'):
    data = {
        "role": "doctor",
        "email": "doctor@mail.ru",
        "password": "doctor"
        }

    response = requests.post(f"http://0.0.0.0:5002/sign_up/", data = json.dumps(data))

@pytest.fixture()
def auth_as_doctor(sign_up_as_doctor, scope = 'module'):
    data = {
        "email": "doctor@mail.ru",
        "password": "doctor"
        }

    response = requests.post(f"http://0.0.0.0:5002/sign_in/", data = json.dumps(data))
    response_json = json.loads(response.text)

    return response_json['access_token']

@pytest.fixture()
def sign_up_as_patient(scope = 'module'):
    data = {
        "role": "patient",
        "email": "patient@mail.ru",
        "password": "patient"
        }

    response = requests.post(f"http://0.0.0.0:5002/sign_up/", data = json.dumps(data))

@pytest.fixture()
def auth_as_patient(sign_up_as_patient, scope = 'module'):
    data = {
        "email": "patient@mail.ru",
        "password": "patient"
        }

    response = requests.post(f"http://0.0.0.0:5002/sign_in/", data = json.dumps(data))
    response_json = json.loads(response.text)

    return response_json['access_token']
