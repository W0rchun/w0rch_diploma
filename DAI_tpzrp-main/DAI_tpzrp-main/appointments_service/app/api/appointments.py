from app.api.models import AppointmentIn, AppointmentOut
from app.api.auth_jwt import decode_token_and_get_user
from fastapi import APIRouter, HTTPException, Request
from app.api import db_manager
from typing import List
import pika
import json
import os


appointments = APIRouter()

RABBITMQ_URL = str(os.getenv("RABBITMQ_URL"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))



@appointments.get('/', response_model=List[AppointmentOut])
async def get_appointments(request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")
    else:
        return await db_manager.get_all_appointments()
    

@appointments.get('/doctor_appointments', response_model=List[AppointmentOut])
async def get_appointments_for_doctor(request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'doctor' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")
    
    if user_date["role"] == 'admin' or user_date["role"] == 'doctor':
        try:
            appointment = await db_manager.get_appointments_for_doctor(user_date["id"])
        except:
            raise HTTPException(status_code=404, detail="appointments for doctor not found")
    
    return appointment


@appointments.get('/{id}', response_model=AppointmentOut)
async def get_appointment(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'doctor' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")
    
    appointment = await db_manager.get_appointment(id)

    if not appointment:
        raise HTTPException(status_code=404, detail="appointment not found")

    if appointment.doctor_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access to update this appointment")
    
    return appointment


@appointments.post('/', status_code=201)
async def add_appointment(payload: AppointmentIn, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'doctor' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")
    
    if payload.doctor_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access to add this doctor")
    
    appointment_id = await db_manager.add_appointment(payload)
    response = {
        'id': appointment_id,
        **payload.dict()
    }

    return response


@appointments.put('/{id}')
async def update_appointment(id: int, payload: AppointmentIn, request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    appointment = await db_manager.get_appointment(id)
    
    if not appointment:
        raise HTTPException(status_code=401, detail="appointment not found")
    if user_date["role"] != 'patient' and user_date["role"] != 'admin' and user_date["role"] != 'doctor':
        raise HTTPException(status_code=402, detail="You have no access to update this appointment")
    if appointment.patient_id != 0 and user_date["role"] != 'admin':
        raise HTTPException(status_code=405, detail="appointment is not free")

    update_data = payload.dict(exclude_unset=True)

    appointment_in_db = AppointmentIn(**appointment)

    updated_appointment = appointment_in_db.copy(update=update_data)

    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_URL, RABBITMQ_PORT, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='appointments')

    data = {
        'region': str(payload.region),
        'medical_institution': payload.medical_institution,
        'subdivision': payload.subdivision,
        'doctor_id': payload.doctor_id,
        'appointment_date': str(payload.appointment_date), 
        'appointment_time': str(payload.appointment_time), 
        'patient_id': int(payload.patient_id),
        'id_in_appointment_service': id
    }

    channel.basic_publish(exchange='', routing_key='appointments', body=json.dumps(data))
    connection.close()

    return await db_manager.update_appointment(id, updated_appointment)


@appointments.delete('/{id}')
async def delete_appointment(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'doctor' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")

    appointment = await db_manager.get_appointment(id)
    
    if not appointment:
        raise HTTPException(status_code=404, detail="appointment not found")
    if appointment.doctor_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access to update this appointment")
    
    return await db_manager.delete_appointment(id)
