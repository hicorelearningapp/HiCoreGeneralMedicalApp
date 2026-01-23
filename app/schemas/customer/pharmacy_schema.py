from pydantic import BaseModel
from typing import Optional

class PharmacyBase(BaseModel):
    Name: Optional[str]
    Address: Optional[str]
    GPSLocation: Optional[str]
    Pincode: Optional[str]
    ImgUrl: Optional[str]
    Contact: Optional[str]
    Email: Optional[str]

    class Config:
        from_attributes = True

class PharmacyCreate(PharmacyBase):
    Name: str

class PharmacyUpdate(BaseModel):
    Name: Optional[str]
    Address: Optional[str]
    GPSLocation: Optional[str]
    Pincode: Optional[str]
    ImgUrl: Optional[str]
    Contact: Optional[str]
    Email: Optional[str]

class PharmacyRead(PharmacyBase):
    PharmacyId: int
    DistanceKm: Optional[float]
