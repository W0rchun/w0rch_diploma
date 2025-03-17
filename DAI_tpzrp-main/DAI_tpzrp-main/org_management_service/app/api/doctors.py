from app.api.auth_jwt import decode_token_and_get_user
from fastapi import APIRouter, HTTPException, Request
from app.api.models import DoctorsIn, DoctorsOut
from app.api import db_manager
from typing import List
import pika
import json
import os

doctors = APIRouter()
RABBITMQ_URL = str(os.getenv("RABBITMQ_URL"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))



@doctors.get('', response_model=List[DoctorsOut])
async def index(request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")
    
    return await db_manager.get_all_doctors()


@doctors.get('/{id}', response_model=DoctorsOut)
async def get_doctor(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'director' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")
    
    doctor = await db_manager.get_doctor(id=id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    elif doctor.director_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access for this doctor")

    return doctor


@doctors.post('', status_code=201)
async def add_doctor(payload: DoctorsIn, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'director' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")

    if payload.director_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access to add this doctor")

    doctor_id = await db_manager.add_doctor(payload)
    
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_URL, RABBITMQ_PORT, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='doctors')
    
    response = {
        'id': doctor_id,
        **payload.dict()
    }

    data = {
        'name': payload.name,
        'subdivision_id': int(payload.subdivision_id)
    }

    channel.basic_publish(exchange='', routing_key='doctors', body=json.dumps(data))
    connection.close()

    return response


@doctors.put('/{id}')
async def update_doctor(id: int, payload: DoctorsIn, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'director' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")

    doctor = await db_manager.get_doctor(id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if doctor.director_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access to update this subdivision")
    if payload.director_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Uncorrect director_id in payload")

    update_data = payload.dict(exclude_unset=True)
    doctor_in_db = DoctorsIn(**doctor)
    updated_doctor = doctor_in_db.copy(update=update_data)

    return await db_manager.update_doctor(id, updated_doctor)


@doctors.delete('/{id}')
async def delete_doctor(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'director' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")
    
    doctor = await db_manager.get_doctor(id)
    
    if not doctor:
        raise HTTPException(status_code=404, detail="DoctorsIn not found")
    elif doctor.director_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access for this doctor")
    
    return await db_manager.delete_doctor(id)
