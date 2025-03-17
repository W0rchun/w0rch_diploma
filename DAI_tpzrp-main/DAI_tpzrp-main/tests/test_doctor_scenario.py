import pytest
import requests
import json
import time


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

def test_add_appointment(auth_as_doctor, order=1):
    response = json.loads(requests.post(f"http://0.0.0.0:5003/", data = json.dumps(data), cookies = {'token': auth_as_doctor}).text)
    response.pop('id')

    assert response == data


def test_appointment_in_doctor_appointments(auth_as_doctor, order=2):
    response = json.loads(requests.get(f"http://0.0.0.0:5003/doctor_appointments/", cookies = {'token': auth_as_doctor}).text)[replace_me-1]
    response.pop('id')

    assert response == data


def test_appointment_by_id(auth_as_doctor, order=3):
    response = json.loads(requests.get(f"http://0.0.0.0:5003/{replace_me}", cookies = {'token': auth_as_doctor}).text)
    response.pop('id')
    
    assert response == data

def test_update_appointment(auth_as_doctor, auth_as_patient, order=4):
    data['patient_id'] = 4
    _ = requests.put(f"http://0.0.0.0:5003/{replace_me}", data = json.dumps(data), cookies = {'token': auth_as_doctor})

    time.sleep(2)
    patient_service_response = json.loads(requests.get(f"http://0.0.0.0:5005/appointments/{replace_me}", cookies = {'token': auth_as_patient}).text)
    time.sleep(5)
    patient_service_response.pop('id')
    data['id_in_appointment_service'] = replace_me

    assert patient_service_response == data

