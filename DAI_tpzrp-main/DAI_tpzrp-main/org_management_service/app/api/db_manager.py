from app.api.db import subdivisions, doctors, database
from app.api.models import SubdivisionIn, DoctorsIn


async def add_subdivision(payload: SubdivisionIn):
    query = subdivisions.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_subdivisions():
    query = subdivisions.select()
    return await database.fetch_all(query=query)


async def get_all_subdivisions_for_director():
    query = subdivisions.select().where(subdivisions.c.director_id==id)
    return await database.fetch_all(query=query)


async def get_subdivision(id):
    query = subdivisions.select().where(subdivisions.c.id==id)
    return await database.fetch_one(query=query)


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


async def get_all_doctors():
    query = doctors.select()
    return await database.fetch_all(query=query)


async def get_doctor(id):
    query = doctors.select().where(doctors.c.id==id)
    return await database.fetch_one(query=query)


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
