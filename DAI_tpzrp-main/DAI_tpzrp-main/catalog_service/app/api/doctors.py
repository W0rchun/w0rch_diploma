from app.api.models import DoctorsIn, DoctorsOut
from fastapi import APIRouter, HTTPException
from app.api import db_manager
from typing import List


doctors = APIRouter()


@doctors.get('/region/{region_id}/organization/{org_id}/subdivision/{subdivision_id}', response_model=List[DoctorsOut])
async def get_doctors(region_id: int, org_id: int, subdivision_id: int):
    # Проверка на существование медицинской организации с указанным region_id и org_id
    med_orgs = await db_manager.get_all_medical_organization(region_id)
    med_org_exists = any(org.id == org_id for org in med_orgs)
    if not med_org_exists:
        raise HTTPException(status_code=404, detail="Medical institution not found for the specified region")

    # Проверка на существование подразделения в указанной мед. организации
    subdivisions = await db_manager.get_all_subdivisions(org_id)
    subdivision_exists = any(subdiv.id == subdivision_id for subdiv in subdivisions)
    if not subdivision_exists:
        raise HTTPException(status_code=404, detail="Subdivision not found for the specified medical institution")

    # Получение докторов для указанного подразделения
    doctors = await db_manager.get_all_doctors(subdivision_id)
    if not doctors:
        raise HTTPException(status_code=404, detail="No doctors found for the specified subdivision")

    return doctors


@doctors.post('', status_code=201)
async def add_doctor(payload: DoctorsIn):
    doctor_id = await db_manager.add_doctor(payload)
    response = {
        'id': doctor_id,
        **payload.dict()
    }

    return response


@doctors.put('/{id}')
async def update_doctor(id: int, payload: DoctorsIn):
    doctor = await db_manager.get_doctor(id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    update_data = payload.dict(exclude_unset=True)
    doctor_in_db = DoctorsIn(**doctor)

    updated_doctor = doctor_in_db.copy(update=update_data)

    return await db_manager.update_doctor(id, updated_doctor)


@doctors.delete('/{id}')
async def delete_doctor(id: int):
    doctor = await db_manager.get_doctor(id)
    if not doctor:
        raise HTTPException(status_code=404, detail="DoctorsIn not found")
    return await db_manager.delete_doctor(id)