from datetime import date, datetime
from ...utils.timezone import ist_now
from pydantic import BaseModel, Field
from typing import Optional


# -------------------------
# Lab Schemas
# -------------------------
class LabBase(BaseModel):
    Name: Optional[str]
    Contact: Optional[str]
    Email: Optional[str]
    Timings: Optional[str]
    Reviews: Optional[str]

    AddressLine1: Optional[str]
    AddressLine2: Optional[str]
    City: Optional[str]
    State: Optional[str]
    Country: Optional[str]
    PostalCode: Optional[str]
    Latitude: Optional[str]
    Longitude: Optional[str]
    ShopPic: Optional[str]

    class Config:
        from_attributes = True


class LabCreate(LabBase):
    Name: str


class LabUpdate(LabBase):
    pass


class LabRead(LabBase):
    LabId: int
    CreatedAt: datetime = Field(default_factory=ist_now)
    UpdatedAt: datetime = Field(default_factory=ist_now)


# -------------------------
# Test Schemas
# -------------------------
class TestBase(BaseModel):
    LabId: Optional[int]
    Name: Optional[str]
    Preparation: Optional[str]
    Price: Optional[float]
    GstPercent: Optional[float]
    Category: Optional[str]
    EstimatedReportTime: Optional[str]

    class Config:
        from_attributes = True


class TestCreate(TestBase):
    LabId: int
    Name: str
    Price: float


class TestUpdate(TestBase):
    pass


class TestRead(TestBase):
    TestId: int
    CreatedAt: datetime = Field(default_factory=ist_now)
    UpdatedAt: datetime = Field(default_factory=ist_now)


# -------------------------
# Appointment Schemas
# -------------------------
class AppointmentBase(BaseModel):
    AppointmentNo: Optional[str]
    LabId: Optional[int]

    PatientName: Optional[str]
    PatientAge: Optional[int]
    PatientGender: Optional[str]
    ContactNumber: Optional[str]
    Email: Optional[str]
    Address: Optional[str]
    GPSLocation: Optional[str]

    AppointmentDate: Optional[date]
    TimeSlot: Optional[str]
    SelectedTests: Optional[str]

    SampleCollectionMode: Optional[str]
    TotalAmount: Optional[float]
    TotalGst: Optional[float]
    NetPayable: Optional[float]
    PaymentMethod: Optional[str]
    PaymentStatus: Optional[str]
    BookingStatus: Optional[str]

    class Config:
        from_attributes = True


class AppointmentCreate(AppointmentBase):
    LabId: int


class AppointmentUpdate(AppointmentBase):
    pass


class AppointmentRead(AppointmentBase):
    AppointmentId: int
    CreatedAt: datetime = Field(default_factory=ist_now)
    UpdatedAt: datetime = Field(default_factory=ist_now)
