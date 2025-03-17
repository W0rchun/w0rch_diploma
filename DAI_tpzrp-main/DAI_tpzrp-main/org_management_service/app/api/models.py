from pydantic import BaseModel
from typing import Optional


class SubdivisionIn(BaseModel):
    name: str
    med_org_id: int
    specialization: str
    director_id: int
    address: str
    contact_number: str


class SubdivisionOut(SubdivisionIn):
    id: int


class SubdivisionUpdate(SubdivisionIn):
    name: Optional[str] = None
    med_org_id: Optional[int] = None
    specialization: Optional[str] = None
    director_id: Optional[int] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None


class DoctorsIn(BaseModel):
    name: str
    position: str
    director_id: int
    subdivision_id: int
    contact_number: str
    email: str


class DoctorsOut(DoctorsIn):
    id: int


class DoctorsUpdate(DoctorsIn):
    name: Optional[str] = None
    position: Optional[str] = None
    director_id: Optional[int] = None
    subdivision_id: Optional[int] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None
