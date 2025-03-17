
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ForeignKey, Date, Time)
from databases import Database
import os

DATABASE_PATIENT_URL = os.getenv("DATABASE_PATIENT_URL")
engine = create_engine(DATABASE_PATIENT_URL)

metadata = MetaData()


appointments = Table(
    'appointments',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('region', String(150)),
    Column('medical_institution', String(150)),
    Column('subdivision', String(150)),
    Column('doctor_id', Integer), 
    Column('appointment_date', Date), 
    Column('appointment_time', Time), 
    Column('patient_id', Integer, nullable = True),
    Column('id_in_appointment_service', Integer),
)


users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('surname', String(50)),
    Column('DoB', String(50)),
    Column('snils', String(50)),
    Column('oms', String(50)),
    Column('email', String(50)),
    Column('phone', String(50)),
)


database = Database(DATABASE_PATIENT_URL)
metadata.create_all(engine)
