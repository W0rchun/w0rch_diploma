from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, Date, Time)
from datetime import date, time
from databases import Database
import os

DATABASE_APPOINT_URL = os.getenv("DATABASE_APPOINT_URL")
engine = create_engine(DATABASE_APPOINT_URL)

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
)

database = Database(DATABASE_APPOINT_URL)