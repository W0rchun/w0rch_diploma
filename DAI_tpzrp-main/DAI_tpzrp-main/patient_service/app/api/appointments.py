from app.api.models import AppointmentIn, AppointmentOut
from app.api.auth_jwt import decode_token_and_get_user
from fastapi import APIRouter, HTTPException, Request
from app.api import db_manager
from typing import List
import pika
import json
import os
import logging

appointments = APIRouter()
RABBITMQ_URL = str(os.getenv("RABBITMQ_URL"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))



@appointments.get('/patient_appointments', response_model=List[AppointmentOut])
async def get_appointments_for_patient(request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'patient' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")

    appointment = await db_manager.get_appointments_for_patient(int(user_date["id"]))
    
    if not appointment:
        raise HTTPException(status_code=404, detail="appointments for patient not found")
    return appointment


@appointments.get('', response_model=List[AppointmentOut])
async def get_all_appointments(request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")

    return await db_manager.get_all_appointments()


@appointments.get('/{id}', response_model=AppointmentOut)
async def get_appointment(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'patient' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")

    appointment = await db_manager.get_appointment(id)
    
    if not appointment:
        raise HTTPException(status_code=404, detail="appointments for patient not found")
    if appointment.patient_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access to update this appointment")
    
    return appointment


@appointments.post('', status_code=201)
async def add_appointment(payload: AppointmentIn, request: Request):
    appointment_id = await db_manager.add_appointment(payload)
    response = {
        'id': appointment_id,
        **payload.dict()
    }

    return response


@appointments.put('/{id}')
async def update_appointment(id: int, payload: AppointmentIn, request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied ")

    appointment = await db_manager.get_appointment(id)
    if not appointment:
        raise HTTPException(status_code=404, detail="appointment not found")

    update_data = payload.dict(exclude_unset=True)
    appointment_in_db = AppointmentIn(**appointment)

    updated_appointment = appointment_in_db.copy(update=update_data)

    return await db_manager.update_appointment(id, updated_appointment)


@appointments.delete('/{id}')
async def delete_appointment(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'patient' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="uncorrect role")
    
    appointment = await db_manager.get_appointment(id)
    if not appointment:
        raise HTTPException(status_code=404, detail="appointment not found")
    
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_URL, RABBITMQ_PORT, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='set_free_appointment')

    access_token = request.cookies['token']

    data = {
        'region': str(appointment.region),
        'medical_institution': appointment.medical_institution,
        'subdivision': appointment.subdivision,
        'doctor_id': appointment.doctor_id,
        'appointment_date': str(appointment.appointment_date), 
        'appointment_time': str(appointment.appointment_time), 
        'patient_id': 0,
        'id_in_appointment_service': appointment.id_in_appointment_service,
        'access_token': access_token
    }

    channel.basic_publish(exchange='', routing_key='set_free_appointment', body=json.dumps(data))
    connection.close()

    return await db_manager.delete_appointment(id)
