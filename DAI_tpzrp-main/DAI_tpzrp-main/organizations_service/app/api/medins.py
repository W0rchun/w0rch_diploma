from app.api.auth_jwt import decode_token_and_get_user
from fastapi import APIRouter, HTTPException, Request
from app.api.models import MedInsIn, MedInsOut
from app.api import db_manager
from typing import List
import pika
import json
import os

medical_instisutions = APIRouter()
RABBITMQ_URL = str(os.getenv("RABBITMQ_URL"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))



@medical_instisutions.get('', response_model=List[MedInsOut])
async def index(request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="uncorrect role")
    
    return await db_manager.get_all_medical_instisutions()


@medical_instisutions.get('/{id}', response_model=MedInsOut)
async def get_medical_instisution(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="uncorrect role")
    
    medical_instisution = await db_manager.get_medical_instisution(id)

    if not medical_instisution:
        raise HTTPException(status_code=404, detail="Medical instisution not found")
    return medical_instisution


@medical_instisutions.post('', status_code=201)
async def add_medical_instisution(payload: MedInsIn, request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="uncorrect role")
    
    medical_instisution_id = await db_manager.add_medical_instisution(payload)
    
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_URL, RABBITMQ_PORT, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='med_orgs')
    
    response = {
        'id': medical_instisution_id,
        **payload.dict()
    }

    data = {
        'name': payload.name,
        'region_id': payload.region_id
    }

    channel.basic_publish(exchange='', routing_key='med_orgs', body=json.dumps(data))
    connection.close()

    return response


@medical_instisutions.put('/{id}')
async def update_medical_instisution(id: int, payload: MedInsIn, request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="uncorrect role")
    
    medical_instisution = await db_manager.get_medical_instisution(id)

    if not medical_instisution:
        raise HTTPException(status_code=404, detail="Medical instisution not found")

    update_data = payload.dict(exclude_unset=True)
    medical_instisution_in_db = MedInsIn(**medical_instisution)

    updated_medical_instisution = medical_instisution_in_db.copy(update=update_data)

    return await db_manager.update_medical_instisution(id, updated_medical_instisution)


@medical_instisutions.delete('/{id}')
async def delete_medical_instisution(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="uncorrect role")
    
    medical_instisution = await db_manager.get_medical_instisution(id)
    
    if not medical_instisution:
        raise HTTPException(status_code=404, detail="MedInsIn not found")
    return await db_manager.delete_medical_instisution(id)
