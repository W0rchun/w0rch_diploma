from app.api.db import appointments, database
from app.api.models import AppointmentIn


async def add_appointment(payload: AppointmentIn):
    query = appointments.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_appointments():
    query = appointments.select()
 
    return await database.fetch_all(query=query)


async def get_appointment(id):
    query = appointments.select().where(appointments.c.id==id)
    return await database.fetch_one(query=query)


async def get_appointments_for_doctor(id):
    query = appointments.select().where(appointments.c.doctor_id==id)
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
