from datetime import date, time
from pydantic import BaseModel
from typing import Optional


class AppointmentIn(BaseModel):
    region: str
    medical_institution: str
    subdivision: str
    doctor_id: int
    appointment_date: date 
    appointment_time: time 
    patient_id: int
    id_in_appointment_service: int


class AppointmentOut(AppointmentIn):
    id: int


class AppointmentUpdate(AppointmentIn):
    region: Optional[str] = None
    medical_institution: Optional[str] = None
    subdivision: Optional[str] = None
    doctor_id: Optional[int] = None
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    patient_id: Optional[int] = None
    id_in_appointment_service: Optional[int] = None


class UserIn(BaseModel):
    personal_id: int
    name: str
    surname: str
    DoB: str
    snils: str
    oms: str
    email: str
    phone: str

class UserOut(UserIn):
    id: int

class UserUpdate(UserIn):
    name: Optional[str] = None
    surname: Optional[str] = None
    DoB: Optional[str] = None
    snils: Optional[str] = None
    oms: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
