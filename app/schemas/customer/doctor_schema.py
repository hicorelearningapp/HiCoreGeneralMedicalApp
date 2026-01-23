from datetime import date, datetime
from ...utils.timezone import ist_now
from typing import Optional
from pydantic import BaseModel, Field


# -------------------------
# Doctor Schemas
# -------------------------
class DoctorBase(BaseModel):
    FirstName: Optional[str]
    LastName: Optional[str]
    Gender: Optional[str]
    DateOfBirth: Optional[str]
    Email: Optional[str]
    MobileNumber: Optional[str]

    Specialization: Optional[str]
    Qualifications: Optional[str]
    ExperienceYears: Optional[int]
    LicenseNumber: Optional[str]

    ClinicName: Optional[str]
    ClinicAddress: Optional[str]
    City: Optional[str]
    State: Optional[str]
    Country: Optional[str]
    PostalCode: Optional[str]

    ConsultationFee: Optional[float]
    AvailableDays: Optional[str]
    AvailableTime: Optional[str]
    SlotDurationMinutes: Optional[int]

    ProfilePhotoUrl: Optional[str]
    About: Optional[str]
    Reviews: Optional[str]
    Status: Optional[str]

    class Config:
        from_attributes = True


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(DoctorBase):
    pass


class DoctorRead(DoctorBase):
    DoctorId: int
    CreatedAt: datetime = Field(default_factory=ist_now)
    UpdatedAt: datetime = Field(default_factory=ist_now)


# -------------------------
# Appointment Schemas
# -------------------------
class DoctorAppointmentBase(BaseModel):
    DoctorId: Optional[int]

    PatientName: Optional[str]
    MobileNumber: Optional[str]
    Age: Optional[int]
    Gender: Optional[str]

    AppointmentMode: Optional[str]
    AppointmentDate: Optional[date]
    AppointmentSlot: Optional[str]
    AppointmentTime: Optional[str]

    Status: Optional[str]
    PaymentStatus: Optional[str]
    PaymentMethod: Optional[str]

    ReasonForVisit: Optional[str]
    Notes: Optional[str]

    class Config:
        from_attributes = True


class DoctorAppointmentCreate(DoctorAppointmentBase):
    DoctorId: int


class DoctorAppointmentUpdate(DoctorAppointmentBase):
    pass


class DoctorAppointmentRead(DoctorAppointmentBase):
    AppointmentId: int
    CreatedAt: datetime = Field(default_factory=ist_now)
    UpdatedAt: datetime = Field(default_factory=ist_now)
