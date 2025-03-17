from app.api.models import MedOrgIn, MedOrgOut
from fastapi import APIRouter, HTTPException
from app.api import db_manager
from typing import List


medical_organization = APIRouter()


@medical_organization.get('/region/{region_id}', response_model=List[MedOrgOut])
async def get_medical_organization(region_id: int):
    # Выполняем асинхронный вызов для получения мед. организации по ID
    medical_organization = await db_manager.get_all_medical_organization(region_id)

    # Проверка, существует ли медицинская организация с данным ID
    if not medical_organization:
        raise HTTPException(status_code=404, detail="Medical organization not found for this region ID")
    
    return medical_organization


@medical_organization.post('', status_code=201)
async def add_medical_organization(payload: MedOrgIn):
    medical_organization_id = await db_manager.add_medical_organization(payload)
    response = {
        'id': medical_organization_id,
        **payload.dict()
    }
    return response


@medical_organization.put('/{id}')
async def update_medical_organization(id: int, payload: MedOrgIn):
    medical_organization = await db_manager.get_medical_organization(id)

    if not medical_organization:
        raise HTTPException(status_code=404, detail="Medical organization not found")

    update_data = payload.dict(exclude_unset=True)
    medical_organization_in_db = MedOrgIn(**medical_organization)
    updated_medical_organization = medical_organization_in_db.copy(update=update_data)

    return await db_manager.update_medical_organization(id, updated_medical_organization)


@medical_organization.delete('/{id}')
async def delete_medical_organization(id: int):
    medical_organization = await db_manager.get_medical_organization(id)

    if not medical_organization:
        raise HTTPException(status_code=404, detail="Medical organization not found")
    return await db_manager.delete_medical_organization(id)
