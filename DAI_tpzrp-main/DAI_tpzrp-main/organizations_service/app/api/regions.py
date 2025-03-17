from app.api.auth_jwt import decode_token_and_get_user
from fastapi import APIRouter, HTTPException, Request
from app.api.models import RegionIn, RegionOut
from app.api import db_manager
from typing import List
import pika
import json
import os

RABBITMQ_URL = str(os.getenv("RABBITMQ_URL"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

regions = APIRouter()


@regions.get('', response_model=List[RegionOut])
async def get_regions(request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="uncorrect role")
    
    return await db_manager.get_all_regions()


@regions.get('/{id}', response_model=RegionOut)
async def get_region(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="uncorrect role")
    
    region = await db_manager.get_region(id)

    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    
    return region


@regions.post('', status_code=201)
async def add_region(payload: RegionIn, request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="uncorrect role")
    
    region_id = await db_manager.add_region(payload)
    
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_URL, RABBITMQ_PORT, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='regions')

    response = {
        'id': region_id,
        **payload.dict()
    }

    data = {
    'name': payload.name,
    }

    channel.basic_publish(exchange='', routing_key='regions', body=json.dumps(data))
    connection.close()

    return response


@regions.put('/{id}')
async def update_region(id: int, payload: RegionIn, request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="uncorrect role")
    
    region = await db_manager.get_region(id)

    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    update_data = payload.dict(exclude_unset=True)
    region_in_db = RegionIn(**region)

    updated_region = region_in_db.copy(update=update_data)

    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_URL, RABBITMQ_PORT, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='regions')

    data = {
        'name': payload.name,
    }

    channel.basic_publish(exchange='', routing_key='regions', body=json.dumps(data))
    connection.close()

    return await db_manager.update_region(id, updated_region)


@regions.delete('/{id}')
async def delete_region(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)
    
    if user_date["role"] != 'admin':
        raise HTTPException(status_code=404, detail="uncorrect role")
    
    region = await db_manager.get_region(id)
    
    if not region:
        raise HTTPException(status_code=404, detail="RegionIn not found")
    return await db_manager.delete_region(id)
