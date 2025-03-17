from typing import List
from fastapi import APIRouter, HTTPException, Request
from app.api.auth_jwt import decode_token_and_get_user
from app.api.models import UserIn, UserOut, UserUpdate
from app.api import db_manager


users = APIRouter()


@users.get('', response_model=List[UserOut])
async def get_users(request: Request):
    user_date = decode_token_and_get_user(request=request)
    if user_date["role"] != "admin":
        raise HTTPException(status_code=404, detail="Permission denied")
    return await db_manager.get_all_users()

@users.get('/{id}', response_model=UserOut)
async def get_user(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] != "admin":
        raise HTTPException(status_code=404, detail="Permission denied")
    
    user = await db_manager.get_user(id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users.post('', status_code=201)
async def add_user(request: Request, payload: UserIn):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] == "admin" or user_date["role"] == "patient":
        user_id = await db_manager.add_user(payload)
        response = {
            'id': user_id,
            **payload.dict()
        }
    else:
        raise HTTPException(status_code=404, detail="Permission denied")
    
    return response

@users.put('/{id}', response_model=UserOut)
async def update_user(id: int, payload: UserUpdate, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] == "admin" or user_date["role"] == "patient":
        user = await db_manager.get_user(id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = payload.dict(exclude_unset=True)
        
        # Обновляем только переданные данные
        updated_user = UserIn(**user).copy(update=update_data)

        # Выполняем обновление в базе данных
        await db_manager.update_user(id, updated_user)

        # Возвращаем обновленные данные
        return {**updated_user.dict(), "id": id}
    else:
        raise HTTPException(status_code=404, detail="Permission denied")


@users.delete('/{id}')
async def delete_user(id: int, request: Request):
    user_date = decode_token_and_get_user(request=request)

    if user_date["role"] == "admin":
        user = await db_manager.get_user(id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=404, detail="Permission denied")
    
    return await db_manager.delete_user(id)

@users.get('/email/{email}', response_model=UserOut)
async def get_user_by_email(email: str):
    user = await db_manager.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
