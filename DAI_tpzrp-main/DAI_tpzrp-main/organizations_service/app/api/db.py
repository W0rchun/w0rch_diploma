from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY, ForeignKey)
from databases import Database
import os

# dbUrl = os.environ["DB_URL"]
# DATABASE_URL = dbUrl


DATABASE_ORG_URL = os.getenv("DATABASE_ORG_URL")
engine = create_engine(DATABASE_ORG_URL)

metadata = MetaData()


regions = Table(
    'regions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(250)),
)


medical_instisutions = Table(
    'medical_instisutions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(150)),
    Column('org_type', String(150)),
    Column('director_id', Integer, nullable=True), # field as ForeignKey
    Column('address', String(250)),
    Column('contact_number', String(11)),
    Column('INN', String(10)),
    Column('KPP', String(9)),
    Column('OGRN', String(9)),
    Column('OKVED', ARRAY(String)),
    Column('licens_number', String(15)),
    Column('region_id', Integer, ForeignKey('regions.id'), nullable=True)
)


database = Database(DATABASE_ORG_URL)
