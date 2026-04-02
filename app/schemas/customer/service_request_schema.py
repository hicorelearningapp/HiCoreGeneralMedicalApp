from datetime import datetime, date
from ...utils.timezone import ist_now
from typing import Optional, Literal
from pydantic import BaseModel, Field


# -------------------------
# Service Request Schemas
# -------------------------
class ServiceRequestBase(BaseModel):
    CustomerId: int
    ServiceProviderId: Optional[int] = None
    ServiceId: Optional[str] = None
    ServiceName: Optional[str] = None

    CustomerName: str
    CustomerPhone: str
    CustomerAddress: str

    PreferredDate: Optional[date] = None
    PreferredTime: Optional[str] = None
    RequestDescription: Optional[str] = None
    WorkLocation: Optional[str] = None

    Status: Literal["pending", "assigned", "accepted", "in_progress", "completed", "cancelled", "rejected"] = "pending"

    AssignedAt: Optional[datetime] = None
    AcceptedAt: Optional[datetime] = None
    CompletedAt: Optional[datetime] = None
    CancelledAt: Optional[datetime] = None

    CustomerNotes: Optional[str] = None
    ProviderNotes: Optional[str] = None

    EstimatedPrice: Optional[float] = None
    FinalPrice: Optional[float] = None
    PaymentStatus: Literal["pending", "paid", "failed"] = "pending"

    AssignmentMode: Literal["random", "visible_profile"] = "random"

    NotificationPreference: Literal["whatsapp", "sms", "both"] = "both"

    class Config:
        from_attributes = True


class ServiceRequestCreate(ServiceRequestBase):
    pass


class ServiceRequestUpdate(BaseModel):
    ServiceProviderId: Optional[int] = None
    Status: Optional[Literal["pending", "assigned", "accepted", "in_progress", "completed", "cancelled", "rejected"]] = None
    AssignedAt: Optional[datetime] = None
    AcceptedAt: Optional[datetime] = None
    CompletedAt: Optional[datetime] = None
    CancelledAt: Optional[datetime] = None
    CustomerNotes: Optional[str] = None
    ProviderNotes: Optional[str] = None
    EstimatedPrice: Optional[float] = None
    FinalPrice: Optional[float] = None
    PaymentStatus: Optional[Literal["pending", "paid", "failed"]] = None
    PreferredDate: Optional[date] = None
    PreferredTime: Optional[str] = None
    RequestDescription: Optional[str] = None

    class Config:
        from_attributes = True


class ServiceRequestRead(ServiceRequestBase):
    RequestId: int
    CreatedAt: datetime = Field(default_factory=ist_now)
    UpdatedAt: datetime = Field(default_factory=ist_now)


# -------------------------
# Assignment Request Schema
# -------------------------
class AssignProviderRequest(BaseModel):
    ServiceProviderId: int
    AssignmentMode: Literal["random", "visible_profile"] = "random"
