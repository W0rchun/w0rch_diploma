from fastapi import Request, HTTPException
import sqlalchemy as _sql
import jwt
import os


JWT_SECRET = os.getenv("JWT_SECRET")
DATABASE_AUTH_URL = os.getenv("DATABASE_AUTH_URL")
engine_auth = _sql.create_engine(DATABASE_AUTH_URL)



def decode_token_and_get_user(request: Request):
    token = request.cookies.get("token")
    try:
        payload = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=["HS256"])
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token, email not found")
        with engine_auth.connect() as connection:
            result = connection.execute(f"SELECT * FROM users WHERE users.email = '{email}'").fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = {
            "id": result.id,
            "role": result.role,
            "email": result.email,
            "date_created": result.date_created
        }
        return user_data
    except jwt.exceptions.DecodeError as e:
        print(f"JWT decoding error: {e}")  # Log the specific error for debugging
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:  # Catch other unexpected exceptions
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")
