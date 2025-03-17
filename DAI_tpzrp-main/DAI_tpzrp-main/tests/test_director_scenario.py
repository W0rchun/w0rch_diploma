import pytest
import requests
import json

replace_me = 1

def test_add_subdivision(auth_as_director, order=1):
    data = {
        "name": "pytest",
        "med_org_id": replace_me,
        "specialization": "pytest",
        "director_id": 2,
        "address": "pytest",
        "contact_number": "pytest"
    }
    
    response = json.loads(requests.post(f"http://0.0.0.0:5001/subdivisions/", data = json.dumps(data), cookies = {'token': auth_as_director}).text)
    response.pop('id')

    assert response == data


def test_subdivision_in_catalog(auth_as_director, order=2):
    catalog_response = json.loads(requests.get(f"http://0.0.0.0:5004/subdivisions/region/{replace_me}/organization/{replace_me}/", cookies = {'token': auth_as_director}).text)[replace_me-1]
    catalog_response.pop('id')

    org_management_response_tmp = json.loads(requests.get(f"http://0.0.0.0:5001/subdivisions/{replace_me}", cookies = {'token': auth_as_director}).text)
    org_management_response = {
        'name': org_management_response_tmp['name'],
        'med_org_id': org_management_response_tmp['med_org_id']
    } 

    assert catalog_response == org_management_response


def test_add_doctor(auth_as_director, order=3):
    data = {
        "name": "pytest",
        "position": "pytest",
        "director_id": 2,
        "subdivision_id": replace_me,
        "contact_number": "pytest",
        "email": "pytest"
    }
    
    response = json.loads(requests.post(f"http://0.0.0.0:5001/doctors/", data = json.dumps(data), cookies = {'token': auth_as_director}).text)
    response.pop('id')
    
    assert response == data

def test_doctor_in_catalog(auth_as_director, order=4):
    catalog_response = json.loads(requests.get(f"http://0.0.0.0:5004/doctors/region/{replace_me}/organization/{replace_me}/subdivision/{replace_me}", cookies = {'token': auth_as_director}).text)[replace_me-1]
    catalog_response.pop('id')

    org_management_response_tmp = json.loads(requests.get(f"http://0.0.0.0:5001/doctors/{replace_me}", cookies = {'token': auth_as_director}).text)
    org_management_response = {
        'name': org_management_response_tmp['name'],
        'subdivision_id': org_management_response_tmp['subdivision_id']
    }
    
    assert catalog_response == org_management_response

