from app.api.models import RegionIn, RegionOut
from fastapi import APIRouter, HTTPException
from app.api import db_manager
from typing import List


regions = APIRouter()


@regions.get('', response_model=List[RegionOut])
async def get_regions():
    return await db_manager.get_all_regions()


@regions.post('', status_code=201)
async def add_region(payload: RegionIn):
    region_id = await db_manager.add_region(payload)
    response = {
        'id': region_id,
        **payload.dict()
    }

    return response


@regions.put('/{id}')
async def update_region(id: int, payload: RegionIn):
    region = await db_manager.get_region(id)

    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    update_data = payload.dict(exclude_unset=True)
    region_in_db = RegionIn(**region)
    updated_region = region_in_db.copy(update=update_data)

    return await db_manager.update_region(id, updated_region)


@regions.delete('/{id}')
async def delete_region(id: int):
    region = await db_manager.get_region(id)

    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return await db_manager.delete_region(id)