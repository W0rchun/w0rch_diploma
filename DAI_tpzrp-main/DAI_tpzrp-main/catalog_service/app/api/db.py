from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY, ForeignKey)
from databases import Database
import os

DATABASE_CATALOG_URL = os.getenv("DATABASE_CATALOG_URL")
engine = create_engine(DATABASE_CATALOG_URL)

metadata = MetaData()


regions = Table(
    'regions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(250)),
)


medical_organization = Table(
    'medical_organization',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(150)),
    Column('region_id', Integer, ForeignKey('regions.id'), nullable=True)
)


subdivisions = Table(
    'subdivisions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(250)),
    Column('med_org_id', Integer, ForeignKey('medical_organization.id'), nullable=True), # field as ForeignKey
)


doctors = Table(
    'doctors',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(150)),
    Column('subdivision_id', Integer, ForeignKey('subdivisions.id'), nullable=True), # field as ForeignKey
)


database = Database(DATABASE_CATALOG_URL)