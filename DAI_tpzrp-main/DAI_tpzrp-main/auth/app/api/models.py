import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
from app.api.database import Base , engine
import app.api.database as _database


Base.metadata.create_all(engine)


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    role = _sql.Column(_sql.String)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)
