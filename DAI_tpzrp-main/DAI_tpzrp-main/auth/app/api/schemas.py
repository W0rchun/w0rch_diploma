import pydantic
import datetime


class UserBase(pydantic.BaseModel):
    role: str
    email: str
    class Config:
       from_attributes=True


class UserCreate(UserBase):
    password: str
    class Config:
       from_attributes=True


class User(UserBase):
    id: int
    date_created: datetime.datetime
    class Config:
       from_attributes=True


class GenerateUserToken(pydantic.BaseModel):
    email: str
    password: str
    class Config:
       from_attributes=True
