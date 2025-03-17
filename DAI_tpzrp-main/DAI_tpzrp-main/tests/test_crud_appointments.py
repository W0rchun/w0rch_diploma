import pytest
import requests
import json

replace_me = 1

data = {
        "region": "pytest",
        "medical_institution": "pytest",
        "subdivision": "pytest",
        "doctor_id": 3,
        "appointment_date": "2024-12-05",
        "appointment_time": "17:17:06.288000",
        "patient_id": 0
    }


def test_add_region(auth_as_admin, order=1):
    region_data = {
        "name": "pytest"
        }
    
    response = json.loads(requests.post(f"http://0.0.0.0:5000/regions/", data = json.dumps(region_data), cookies = {'token': auth_as_admin}).text)
    response.pop('id')
    
    assert response == region_data


def test_add_medorg(auth_as_admin, order=2):
    medorg_data = {
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
    
    response = json.loads(requests.post(f"http://0.0.0.0:5000/organizations/", data = json.dumps(medorg_data), cookies = {'token': auth_as_admin}).text)
    response.pop('id')

    assert response == medorg_data


def test_add_subdivision(auth_as_director, order=3):
    subdiv_data = {
        "name": "pytest",
        "med_org_id": replace_me,
        "specialization": "pytest",
        "director_id": 2,
        "address": "pytest",
        "contact_number": "pytest"
    }
    
    response = json.loads(requests.post(f"http://0.0.0.0:5001/subdivisions/", data = json.dumps(subdiv_data), cookies = {'token': auth_as_director}).text)
    response.pop('id')

    assert response == subdiv_data


def test_add_doctor(auth_as_director, order=4):
    doctor_data = {
        "name": "pytest",
        "position": "pytest",
        "director_id": 2,
        "subdivision_id": replace_me,
        "contact_number": "pytest",
        "email": "pytest"
    }
    
    response = json.loads(requests.post(f"http://0.0.0.0:5001/doctors/", data = json.dumps(doctor_data), cookies = {'token': auth_as_director}).text)
    response.pop('id')
    
    assert response == doctor_data


def test_add_appointment(auth_as_doctor, order=5):
    response = json.loads(requests.post(f"http://0.0.0.0:5003/", data = json.dumps(data), cookies = {'token': auth_as_doctor}).text)
    response.pop('id')

    assert response == data

def test_get_appointment(auth_as_doctor, order=6):
    response = json.loads(requests.get(f"http://0.0.0.0:5003/{replace_me}", cookies = {'token': auth_as_doctor}).text)
    response.pop('id')

    assert response == data

def test_appointment_in_doctor_appointments(auth_as_doctor, order=7):
    response = json.loads(requests.get(f"http://0.0.0.0:5003/doctor_appointments/", cookies = {'token': auth_as_doctor}).text)[replace_me-1]
    response.pop('id')

    assert response == data


def test_put_appointment(auth_as_admin, order=8):
    data['region'] = 'pytest2'
    _ = json.loads((requests.put(f"http://0.0.0.0:5003/{replace_me}", data = json.dumps(data), cookies = {'token': auth_as_admin})).text)

    response = json.loads(requests.get(f"http://0.0.0.0:5003/{replace_me}", data = json.dumps(data), cookies = {'token': auth_as_admin}).text)
    response.pop('id')

    assert response == data
    

@pytest.mark.xfail()
def test_delete_appointment(auth_as_doctor, order=9):
    _ = requests.delete(f"http://0.0.0.0:5003/{replace_me}", cookies = {'token': auth_as_doctor})
    response = json.loads(requests.get(f"http://0.0.0.0:5003/{replace_me}", cookies = {'token': auth_as_doctor}).text)

    assert response == data
    
    
