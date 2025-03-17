from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, BLANK_SCHEMA, schema)
from databases import Database
import os

DATABASE_ORG_MANAGE_URL = os.getenv("DATABASE_ORG_MANAGE_URL")
engine = create_engine(DATABASE_ORG_MANAGE_URL)
metadata = MetaData()



subdivisions = Table(
    'subdivisions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(250)),
    Column('med_org_id', Integer, nullable=True), # field as ForeignKey
    Column('specialization', String(150)),
    Column('director_id', Integer, nullable=True), # field as ForeignKey
    Column('address', String(250)),
    Column('contact_number', String(11)),
)


doctors = Table(
    'doctors',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(150)),
    Column('position', String(150)),
    Column('director_id', Integer, nullable=True), # field as ForeignKey
    Column('subdivision_id', Integer, nullable=True), # field as ForeignKey
    Column('contact_number', String(11)),
    Column('email', String(50)),
    Column('login', String(50)),
    Column('password', String(50)),
)


database = Database(DATABASE_ORG_MANAGE_URL)
