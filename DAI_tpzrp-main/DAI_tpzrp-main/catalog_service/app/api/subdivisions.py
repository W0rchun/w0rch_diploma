from app.api.models import SubdivisionIn, SubdivisionOut
from fastapi import APIRouter, HTTPException
from app.api import db_manager
from typing import List


subdivisions = APIRouter()


@subdivisions.get('/region/{region_id}/organization/{org_id}', response_model=List[SubdivisionOut])
async def get_subdivisions(region_id: int, org_id: int):
    # Ожидаем результат выполнения асинхронного вызова
    med_orgs = await db_manager.get_all_medical_organization(region_id)
    
    # Проверка на существование мед. организации с указанными region_id и org_id
    med_org_exists = any(org.id == org_id for org in med_orgs)
    if not med_org_exists:
        raise HTTPException(status_code=404, detail="Medical organization not found for the specified region and ID")

    # Получение подразделений
    subdivisions = await db_manager.get_all_subdivisions(org_id)
    if not subdivisions:
        raise HTTPException(status_code=404, detail="No subdivisions found for the specified medical organization")

    return subdivisions


@subdivisions.post('', status_code=201)
async def add_subdivision(payload: SubdivisionIn):
    subdivision_id = await db_manager.add_subdivision(payload)
    response = {
        'id': subdivision_id,
        **payload.dict()
    }

    return response


@subdivisions.put('/{id}')
async def update_subdivision(id: int, payload: SubdivisionIn):
    subdivision = await db_manager.get_subdivision(id)

    if not subdivision:
        raise HTTPException(status_code=404, detail="Subdivision not found")

    update_data = payload.dict(exclude_unset=True)
    subdivision_in_db = SubdivisionIn(**subdivision)

    updated_subdivision = subdivision_in_db.copy(update=update_data)

    return await db_manager.update_subdivision(id, updated_subdivision)


@subdivisions.delete('/{id}')
async def delete_subdivision(id: int):
    subdivision = await db_manager.get_subdivision(id)
    
    if not subdivision:
        raise HTTPException(status_code=404, detail="SubdivisionIn not found")
    return await db_manager.delete_subdivision(id)