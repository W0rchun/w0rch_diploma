from pydantic import BaseModel
from typing import Optional


class RegionIn(BaseModel):
    name: str


class RegionOut(RegionIn):
    id: int


class RegionUpdate(RegionIn):
    name: Optional[str] = None


class MedOrgIn(BaseModel):
    name: str
    region_id: int


class MedOrgOut(MedOrgIn):
    id: int


class MedOrgUpdate(MedOrgIn):
    name: Optional[str] = None
    region_id: Optional[int] = None 


class SubdivisionIn(BaseModel):
    name: str
    med_org_id: int


class SubdivisionOut(SubdivisionIn):
    id: int
    med_org_id: int


class SubdivisionUpdate(SubdivisionIn):
    name: Optional[str] = None
    med_org_id: Optional[int] = None


class DoctorsIn(BaseModel):
    name: str
    subdivision_id: int


class DoctorsOut(DoctorsIn):
    id: int
    subdivision_id: int


class DoctorsUpdate(DoctorsIn):
    name: Optional[str] = None
    subdivision_id: Optional[int] = None
