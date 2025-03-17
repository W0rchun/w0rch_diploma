import jwt
import fastapi as _fastapi
from sqlalchemy import select
from app.api.database import engine
import app.api.models as _models
import os

JWT_SECRET = os.getenv("JWT_SECRET")


async def decode_jwt_token_and_get_user(token: str):
    try:
        # Декодируем JWT-токен
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        
        # Извлекаем email из полезной нагрузки
        email = payload.get("email")
        if not email:
            raise _fastapi.HTTPException(status_code=401, detail="Invalid token, email not found")

        # Выполняем запрос к базе данных без использования ORM
        with engine.connect() as connection:
            query = select(_models.User).where(_models.User.email == email)
            result = connection.execute(query).fetchone()

        if not result:
            raise _fastapi.HTTPException(status_code=404, detail="User not found")

        # Преобразуем результат в словарь для ответа
        user_data = {
            "id": result.id,
            "role": result.role,
            "email": result.email,
            "date_created": result.date_created
        }
        
        return user_data
    except jwt.InvalidTokenError:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid token")