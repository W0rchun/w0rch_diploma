import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
import os

DATABASE_AUTH_URL = os.getenv("DATABASE_AUTH_URL")

# Коннектим бд 
engine = _sql.create_engine(DATABASE_AUTH_URL)
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = _declarative.declarative_base()
