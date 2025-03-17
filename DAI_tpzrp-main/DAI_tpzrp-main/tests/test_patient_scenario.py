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
        "patient_id": 4,
        "id_in_appointment_service": 1
    }


def test_appointment_in_doctor_appointments(auth_as_patient, order=1):
    response = json.loads(requests.get(f"http://0.0.0.0:5005/appointments/patient_appointments/", cookies = {'token': auth_as_patient}).text)[replace_me-1]
    response.pop('id')

    assert response == data


def test_appointment_by_id(auth_as_patient, order=2):
    response = json.loads(requests.get(f"http://0.0.0.0:5005/appointments/{replace_me}", cookies = {'token': auth_as_patient}).text)
    response.pop('id')
    
    assert response == data

def test_delete_appointment(auth_as_admin, auth_as_patient, order=3):
    data['patient_id'] = 0
    data.pop('id_in_appointment_service')
    _ = requests.delete(f"http://0.0.0.0:5005/appointments/{replace_me}", cookies = {'token': auth_as_patient})

    time.sleep(2)
    appointments_service_response = json.loads(requests.get(f"http://0.0.0.0:5003/{replace_me}", cookies = {'token': auth_as_admin}).text)
    time.sleep(5)
    
    appointments_service_response.pop('id')
    
    assert appointments_service_response == data

