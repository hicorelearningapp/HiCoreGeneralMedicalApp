from datetime import datetime
from ...utils.timezone import ist_now
from typing import Optional, Literal
from pydantic import BaseModel, Field


# -------------------------
# Service Provider Schemas
# -------------------------
class ServiceProviderBase(BaseModel):
    ServiceId: Optional[str] = None
    ServiceName: Optional[str] = None
    ProviderName: Optional[str] = None

    PhotoUrl: Optional[str] = None
    CertificateUrl: Optional[str] = None
    AadhaarOrIdProofUrl: Optional[str] = None

    Address: str
    WorkLocation: str
    State: str
    Pincode: str

    PhoneNumber: str
    Email: str

    ExperienceYears: int
    Gender: str
    DateOfBirth: str
    LicenseNumber: Optional[str] = None

    AvailabilityStatus: Literal["available", "unavailable", "busy"] = "available"
    Rating: Optional[float] = 0.0
    IsVerified: Optional[bool] = False
    IsActive: Optional[bool] = True

    Specialization: str
    ServiceDescription: str
    ServiceCategory: str

    ProfileCompleted: Optional[bool] = False

    class Config:
        from_attributes = True


class ServiceProviderCreate(ServiceProviderBase):
    ServiceId: str
    ServiceName: str
    ProviderName: str


class ServiceProviderUpdate(ServiceProviderBase):
    pass


class ServiceProviderRead(ServiceProviderBase):
    ServiceProviderId: int
    CreatedAt: datetime = Field(default_factory=ist_now)
    UpdatedAt: datetime = Field(default_factory=ist_now)
