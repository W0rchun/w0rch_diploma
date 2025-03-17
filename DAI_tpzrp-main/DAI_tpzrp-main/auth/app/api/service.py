import jwt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import email_validator as _email_check
import fastapi as _fastapi
import fastapi.security as _security
from passlib.hash import bcrypt
import app.api.database as _database
import app.api.schemas as _schemas
import app.api.models as _models
import os

# Загружаем environment variables
JWT_SECRET = os.getenv("JWT_SECRET")

oauth2schema = _security.OAuth2PasswordBearer("/api/token")


def create_database():
    # Создаём таблицы в бд
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Извлечь юзера по email из бд
async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()


# Создать юзера
async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    try:
        valid = _email_check.validate_email(user.email)
        role = user.role
        email = valid.email
    except _email_check.EmailNotValidError:
        raise _fastapi.HTTPException(status_code=404, detail="Please enter a valid email")
    if role != "patient" and role != "doctor" and role!= "admin" and role!= "director":
        raise _fastapi.HTTPException(status_code=404, detail="Please enter a valid role")

    user_obj = _models.User(email=email, role=role, hashed_password=_hash.bcrypt.hash(user.password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


# Аутентификация юзера
async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(email=email, db=db)

    if not user:
        return False
    
    if not user.verify_password(password):
        return False

    return user


# Сгенерить токен
async def create_token(response: _fastapi.Response, user: _models.User):
    user_obj = _schemas.User.from_orm(user)
    user_dict = user_obj.model_dump()
    del user_dict["date_created"]
    token = jwt.encode(user_dict, JWT_SECRET, algorithm="HS256")
    response.set_cookie(key='token', value=token)
    return dict(access_token=token, token_type="bearer")


# Получить текущего аутентифицированного пользователя из токена JWT
async def get_current_user(db: _orm.Session = _fastapi.Depends(get_db), token: str = _fastapi.Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Email or Password")
    return _schemas.User.from_orm(user)
