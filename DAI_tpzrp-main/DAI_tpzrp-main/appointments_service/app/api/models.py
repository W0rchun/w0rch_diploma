from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import DATETIME
from datetime import date, time
import sqlalchemy as _sql


class AppointmentIn(BaseModel):
    region: str
    medical_institution: str
    subdivision: str
    doctor_id: int
    appointment_date: date 
    appointment_time: time 
    patient_id: int


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
