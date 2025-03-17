from app.api.db import users, appointments, database
from app.api.models import UserIn, AppointmentIn


async def add_user(payload: UserIn):
    query = users.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_users():
    query = users.select().order_by(users.c.id)
    return await database.fetch_all(query=query)


async def get_user(id: int):
    query = users.select().where(users.c.id == id)
    return await database.fetch_one(query=query)

async def update_user(id: int, payload: UserIn):
    query = (
        users
        .update()
        .where(users.c.id == id)
        .values(**payload.dict())
    )
    await database.execute(query=query)
    return await get_user(id)


async def delete_user(id: int):
    query = users.delete().where(users.c.id == id)
    return await database.execute(query=query)


async def add_appointment(payload: AppointmentIn):
    query = appointments.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_appointments():
    query = appointments.select()
    return await database.fetch_all(query=query)


async def get_appointment(id):
    query = appointments.select().where(appointments.c.id==id)
    return await database.fetch_one(query=query)


async def get_appointments_for_patient(id):
    query = appointments.select().where(appointments.c.patient_id==id)
    return await database.fetch_all(query=query)


async def delete_appointment(id: int):
    query = appointments.delete().where(appointments.c.id==id)
    return await database.execute(query=query)


async def update_appointment(id: int, payload: AppointmentIn):
    query = (
        appointments
        .update()
        .where(appointments.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)
