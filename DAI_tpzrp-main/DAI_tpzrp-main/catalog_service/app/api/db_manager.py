from app.api.db import regions, medical_organization, subdivisions, doctors, database
from app.api.models import RegionIn, MedOrgIn, SubdivisionIn, DoctorsIn


async def add_region(payload: RegionIn):
    query = regions.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_regions():
    query = regions.select()
    return await database.fetch_all(query=query)


async def delete_region(id: int):
    query = regions.delete().where(regions.c.id==id)
    return await database.execute(query=query)


async def update_region(id: int, payload: RegionIn):
    query = (
        regions
        .update()
        .where(regions.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)


async def add_medical_organization(payload: MedOrgIn):
    query = medical_organization.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_medical_organization(region_id: int):
    query = medical_organization.select().where(medical_organization.c.region_id == region_id)
    return await database.fetch_all(query=query)


async def delete_medical_organization(id: int):
    query = medical_organization.delete().where(medical_organization.c.id==id)
    return await database.execute(query=query)


async def update_medical_organization(id: int, payload: MedOrgIn):
    query = (
        medical_organization
        .update()
        .where(medical_organization.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)


async def add_subdivision(payload: SubdivisionIn):
    query = subdivisions.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_subdivisions(med_org_id: int):
    query = subdivisions.select().where(subdivisions.c.med_org_id == med_org_id)
    return await database.fetch_all(query=query)


async def delete_subdivision(id: int):
    query = subdivisions.delete().where(subdivisions.c.id==id)
    return await database.execute(query=query)


async def update_subdivision(id: int, payload: SubdivisionIn):
    query = (
        subdivisions
        .update()
        .where(subdivisions.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)


async def add_doctor(payload: DoctorsIn):
    query = doctors.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_doctors(subdivision_id: int):
    query = doctors.select().where(doctors.c.subdivision_id == subdivision_id)
    return await database.fetch_all(query=query)


async def delete_doctor(id: int):
    query = doctors.delete().where(doctors.c.id==id)
    return await database.execute(query=query)


async def update_doctor(id: int, payload: DoctorsIn):
    query = (
        doctors
        .update()
        .where(doctors.c.id == id)
        .values(**payload.dict())
    )
    
    return await database.execute(query=query)
