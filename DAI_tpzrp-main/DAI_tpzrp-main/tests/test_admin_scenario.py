import pytest
import requests
import json

replace_me = 1


def test_add_region(auth_as_admin, order=1):
    data = {
        "name": "pytest"
        }
    
    response = json.loads(requests.post(f"http://0.0.0.0:5000/regions/", data = json.dumps(data), cookies = {'token': auth_as_admin}).text)
    response.pop('id')
    
    assert response == data


def test_region_in_catalog(auth_as_admin, order=2):
    catalog_response = json.loads(requests.get(f"http://0.0.0.0:5004/regions/", cookies = {'token': auth_as_admin}).text)
    organizations_service_response = json.loads(requests.get(f"http://0.0.0.0:5000/regions/{replace_me}", cookies = {'token': auth_as_admin}).text)

    assert catalog_response[replace_me-1] == organizations_service_response


def test_add_medorg(auth_as_admin, order=3):
    data = {
        "name": "pytest",
        "org_type": "pytest",
        "director_id": 2,
        "address": "pytest",
        "contact_number": "pytest",
        "INN": "pytest",
        "KPP": "pytest",
        "OGRN": "pytest",
        "OKVED": [
        "pytest"
        ],
        "licens_number": "pytest",
        "region_id": replace_me
    }
    
    response = json.loads(requests.post(f"http://0.0.0.0:5000/organizations/", data = json.dumps(data), cookies = {'token': auth_as_admin}).text)
    response.pop('id')

    assert response == data

    
def test_medorg_in_catalog(auth_as_admin, order=4):
    catalog_response = json.loads(requests.get(f"http://0.0.0.0:5004//organizations/region/{replace_me}/", cookies = {'token': auth_as_admin}).text)[replace_me-1]
    catalog_response.pop('id')

    organizations_service_response_tmp = json.loads(requests.get(f"http://0.0.0.0:5000//organizations/{replace_me}", cookies = {'token': auth_as_admin}).text)
    organizations_service_response = {
        'name': organizations_service_response_tmp['name'],
        'region_id': organizations_service_response_tmp['region_id']
    }
    
    assert catalog_response == organizations_service_response


