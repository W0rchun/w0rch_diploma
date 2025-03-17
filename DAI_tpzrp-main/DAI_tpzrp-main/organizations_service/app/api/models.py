from typing import List, Optional
from pydantic import BaseModel


class RegionIn(BaseModel):
    name: str


class RegionOut(RegionIn):
    id: int


class RegionUpdate(RegionIn):
    name: Optional[str] = None


class MedInsIn(BaseModel):
    name: str
    org_type: str
    director_id: int
    address: str
    contact_number: str
    INN: str
    KPP: str
    OGRN: str
    OKVED: List[str]
    licens_number: str
    region_id: int


class MedInsOut(MedInsIn):
    id: int


class MedInsUpdate(MedInsIn):
    name: Optional[str] = None
    org_type: Optional[str] = None
    director_id: Optional[int] = None 
    address: Optional[str] = None
    contact_number: Optional[str] = None
    INN: Optional[str] = None
    KPP: Optional[str] = None
    OGRN: Optional[str] = None
    KOVED: Optional[List[str]] = None
    licens_number: Optional[str] = None
    region_id: Optional[int] = None 


class SubdivisionIn(BaseModel):
    name: str
    specialization: str
    director_id: int
    address: str
    contact_number: str


class SubdivisionOut(SubdivisionIn):
    id: int


class SubdivisionUpdate(SubdivisionIn):
    name: Optional[str] = None
    specialization: Optional[str] = None
    director_id: Optional[int] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None


class DoctorsIn(BaseModel):
    name: str
    position: str
    subdivision_id: int
    contact_number: str
    email: str
    login: str
    password: str



class DoctorsOut(DoctorsIn):
    id: int


class DoctorsUpdate(DoctorsIn):
    name: Optional[str] = None
    position: Optional[str] = None
    subdivision_id: Optional[int] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None
