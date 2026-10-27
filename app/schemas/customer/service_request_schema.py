from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime


class ServiceRequestBase(BaseModel):
    CustomerId: Optional[int] = None
    ServiceProviderId: Optional[int] = None
    ServiceListId: Optional[int] = None
    ProviderServiceId: Optional[int] = None

    CustomerName: Optional[str] = None
    CustomerPhone: Optional[str] = None
    CustomerAddress: Optional[str] = None
    Pincode: Optional[str] = None

    PreferredDate: Optional[date] = None
    PreferredStartTime: Optional[str] = None
    PreferredEndTime: Optional[str] = None

    RequestDescription: Optional[str] = None
    Status: Optional[str] = "pending"

    FinalPrice: Optional[float] = None
    AssignmentMode: Optional[str] = None
    NotificationPreference: Optional[str] = None

    class Config:
        from_attributes = True


class ServiceRequestCreate(ServiceRequestBase):
    pass


class ServiceRequestUpdate(ServiceRequestBase):
    pass


class ServiceRequestRead(ServiceRequestBase):
    ServiceRequestId: int
    CreatedAt: Optional[datetime]
    UpdatedAt: Optional[datetime]