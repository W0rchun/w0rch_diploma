from fastapi import HTTPException, Response, Request, Cookie
import app.api.database as _database
import app.api.service as _services
import app.api.schemas as _schemas
import app.api.models as _models
import app.api.auth_jwt as _auth
import sqlalchemy.orm as _orm
import fastapi as _fastapi
import logging


app = _fastapi.FastAPI()
logging.basicConfig(level=logging.INFO)
_models.Base.metadata.create_all(_models.engine)


# Проверяем конект к БД
def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Создание пользователя
@app.post("/sign_up", tags = ['User Auth'])
async def create_user(
    user: _schemas.UserCreate, 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(email=user.email, db=db)

    if db_user:
        logging.info('User with that email already exists')
        raise _fastapi.HTTPException(
            status_code=200,
            detail="User with that email already exists")
    
    user = await _services.create_user(user=user, db=db)

    return _fastapi.HTTPException(
            status_code=201,
            detail="User Registered!")


# Endpoint проверки живности API
@app.get("/check_api", tags = ['Api check'])
async def check_api():
    return {"status": "API is alive."}


# Создание токена
@app.post("/sign_in", tags = ['User Auth'])
async def generate_token(
    response: Response,
    user_data: _schemas.GenerateUserToken,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user = await _services.authenticate_user(email=user_data.email, password=user_data.password, db=db)

    if not user:
        logging.info('Invalid Credentials')
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Credentials")
    
    logging.info('JWT Token Generated')
    return await _services.create_token(response=response, user=user)


# Выход из аккаунта
@app.get("/logout", tags = ['User Auth'])
async def logout(response: Response):
    response.delete_cookie(key="token")
    return {"massage": "Logout compliete."}


@app.get("/decode_token_and_get_user", tags=['User Auth'])
async def decode_token_and_get_user(request: _fastapi.Request):
    token = request.cookies.get("token")
    user = await _auth.decode_jwt_token_and_get_user(token=token)
    return user

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5002, reload=True)
