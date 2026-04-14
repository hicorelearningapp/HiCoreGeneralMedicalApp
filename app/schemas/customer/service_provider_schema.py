from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ServiceProviderBase(BaseModel):
    ProviderName: Optional[str] = None
    PhotoUrl: Optional[str] = None
    Address: Optional[str] = None
    Pincode: Optional[str] = None
    PhoneNumber: Optional[str] = None
    Email: Optional[str] = None
    ExperienceYears: Optional[int] = None
    Gender: Optional[str] = None
    DateOfBirth: Optional[date] = None
    AvailabilityStatus: Optional[str] = None
    Rating: Optional[float] = None
    Specialization: Optional[str] = None
    ServiceDescription: Optional[str] = None

    class Config:
        from_attributes = True


class ServiceProviderCreate(ServiceProviderBase):
    Password: Optional[str]


class ServiceProviderUpdate(ServiceProviderBase):
    Password: Optional[str] = None


class ServiceProviderRead(ServiceProviderBase):
    ServiceProviderId: int
    CreatedAt: Optional[datetime]
    UpdatedAt: Optional[datetime]


class ProviderRegisterSchema(BaseModel):
    Email: Optional[str]
    Password: Optional[str]


class ProviderLoginSchema(BaseModel):
    Email: Optional[str]
    Password: Optional[str]