from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from ...utils.timezone import ist_now
from .sql_base import Base


# -------------------------------------------------
# Doctor Model
# -------------------------------------------------
class Doctor(Base):
    __tablename__ = "Doctor"

    DoctorId = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String, nullable=False)
    LastName = Column(String, nullable=False)
    Gender = Column(String, nullable=True)
    DateOfBirth = Column(String, nullable=True)
    Email = Column(String, nullable=True)
    MobileNumber = Column(String, nullable=True)

    Specialization = Column(String, nullable=True)
    Qualifications = Column(String, nullable=True)
    ExperienceYears = Column(Integer, nullable=True)
    LicenseNumber = Column(String, nullable=True)

    ClinicName = Column(String, nullable=True)
    ClinicAddress = Column(String, nullable=True)
    City = Column(String, nullable=True)
    State = Column(String, nullable=True)
    Country = Column(String, nullable=True)
    PostalCode = Column(String, nullable=True)

    ConsultationFee = Column(Float, nullable=True, default=0.0)
    AvailableDays = Column(String, nullable=True)
    AvailableTime = Column(String, nullable=True)
    SlotDurationMinutes = Column(Integer, nullable=True)

    ProfilePhotoUrl = Column(String, nullable=True)
    About = Column(String, nullable=True)
    Reviews = Column(String, nullable=True)
    Status = Column(String, nullable=True)   # Active / Inactive

    CreatedAt = Column(DateTime, default=ist_now)
    UpdatedAt = Column(DateTime, default=ist_now)


# -------------------------------------------------
# Doctor Appointment Model
# -------------------------------------------------
class DoctorAppointment(Base):
    __tablename__ = "DoctorAppointment"

    AppointmentId = Column(Integer, primary_key=True, index=True)
    DoctorId = Column(Integer, nullable=False)

    PatientName = Column(String, nullable=True)
    MobileNumber = Column(String, nullable=True)
    Age = Column(Integer, nullable=True)
    Gender = Column(String, nullable=True)

    AppointmentMode = Column(String, nullable=True)    # Clinic / Home / Video
    AppointmentDate = Column(Date, nullable=True)
    AppointmentSlot = Column(String, nullable=True)
    AppointmentTime = Column(String, nullable=True)

    Status = Column(String, nullable=True)
    PaymentStatus = Column(String, nullable=True)
    PaymentMethod = Column(String, nullable=True)

    ReasonForVisit = Column(String, nullable=True)
    Notes = Column(String, nullable=True)

    CreatedAt = Column(DateTime, default=ist_now)
    UpdatedAt = Column(DateTime, default=ist_now)
