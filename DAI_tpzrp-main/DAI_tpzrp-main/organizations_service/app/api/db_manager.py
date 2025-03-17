from app.api.db import regions, medical_instisutions, database
from app.api.models import RegionIn, MedInsIn


async def add_region(payload: RegionIn):
    query = regions.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_regions():
    query = regions.select()
    return await database.fetch_all(query=query)


async def get_region(id):
    query = regions.select().where(regions.c.id==id)
    return await database.fetch_one(query=query)


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


async def add_medical_instisution(payload: MedInsIn):
    query = medical_instisutions.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_medical_instisutions():
    query = medical_instisutions.select()
    return await database.fetch_all(query=query)


async def get_medical_instisution(id):
    query = medical_instisutions.select().where(medical_instisutions.c.id==id)
    return await database.fetch_one(query=query)


async def delete_medical_instisution(id: int):
    query = medical_instisutions.delete().where(medical_instisutions.c.id==id)
    return await database.execute(query=query)


async def update_medical_instisution(id: int, payload: MedInsIn):
    query = (
        medical_instisutions
        .update()
        .where(medical_instisutions.c.id == id)
        .values(**payload.dict())
    )
    
    return await database.execute(query=query)