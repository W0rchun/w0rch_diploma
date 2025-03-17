from app.api.models import SubdivisionIn, SubdivisionOut
from fastapi import APIRouter, HTTPException, Request
from app.api.auth_jwt import decode_token_and_get_user
from app.api import db_manager
from typing import List
import pika
import json
import os

subdivisions = APIRouter()
RABBITMQ_URL = str(os.getenv("RABBITMQ_URL"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))



@subdivisions.get('', response_model=List[SubdivisionOut])
async def get_subdivisions(request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")
    
    return await db_manager.get_all_subdivisions()


@subdivisions.get('/{id}', response_model=SubdivisionOut)
async def get_subdivision(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'director' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")
    
    subdivision = await db_manager.get_subdivision(id)

    if not subdivision:
        raise HTTPException(status_code=404, detail="Subdivision not found")
    elif subdivision.director_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access for this subdivision")
    
    return subdivision


@subdivisions.post('', status_code=201)
async def add_subdivision(payload: SubdivisionIn, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'director' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")

    if payload.director_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access to add this subdivision")
    
    subdivision_id = await db_manager.add_subdivision(payload)
    
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_URL, RABBITMQ_PORT, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='subdivisions')
    
    response = {
        'id': subdivision_id,
        **payload.dict()
    }

    data = {
        'name': payload.name,
        'med_org_id': int(payload.med_org_id)
    }

    channel.basic_publish(exchange='', routing_key='subdivisions', body=json.dumps(data))
    connection.close()

    return response


@subdivisions.put('/{id}')
async def update_subdivision(id: int, payload: SubdivisionIn, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'director' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")

    subdivision = await db_manager.get_subdivision(id)
    if not subdivision:
        raise HTTPException(status_code=404, detail="Subdivision not found")
    if subdivision.director_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access to update this subdivision")
    if payload.director_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Uncorrect director_id in payload")

    update_data = payload.dict(exclude_unset=True)
    subdivision_in_db = SubdivisionIn(**subdivision)

    updated_subdivision = subdivision_in_db.copy(update=update_data)

    return await db_manager.update_subdivision(id, updated_subdivision)


@subdivisions.delete('/{id}')
async def delete_subdivision(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != 'director' and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="Permission denied")

    subdivision = await db_manager.get_subdivision(id)

    if not subdivision:
        raise HTTPException(status_code=404, detail="SubdivisionIn not found")
    elif subdivision.director_id != user_date["id"] and user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="You have no access to delete this subdivision")
    
    return await db_manager.delete_subdivision(id)
