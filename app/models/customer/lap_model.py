from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from ...utils.timezone import ist_now
from .sql_base import Base

# -------------------------
# Lab Model
# -------------------------
class Lab(Base):
    __tablename__ = "Lab"

    LabId = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)
    Contact = Column(String, nullable=True)
    Email = Column(String, nullable=True)
    Timings = Column(String, nullable=True)
    Reviews = Column(String, nullable=True)  

    AddressLine1 = Column(String, nullable=True)
    AddressLine2 = Column(String, nullable=True)
    City = Column(String, nullable=True)
    State = Column(String, nullable=True)
    Country = Column(String, nullable=True)
    PostalCode = Column(String, nullable=True)
    Latitude = Column(String, nullable=True)
    Longitude = Column(String, nullable=True)
    ShopPic = Column(String, nullable=True)

    CreatedAt = Column(DateTime, default=ist_now)
    UpdatedAt = Column(DateTime, default=ist_now)


# -------------------------
# Test Model
# -------------------------
class Test(Base):
    __tablename__ = "Test"

    TestId = Column(Integer, primary_key=True, index=True)
    LabId = Column(Integer, nullable=False)
    Name = Column(String, nullable=False)
    Preparation = Column(String, nullable=True)
    Price = Column(Float, nullable=False, default=0.0)
    GstPercent = Column(Float, nullable=True, default=0.0)
    Category = Column(String, nullable=True)
    EstimatedReportTime = Column(String, nullable=True)

    CreatedAt = Column(DateTime, default=ist_now)
    UpdatedAt = Column(DateTime, default=ist_now)


# -------------------------
# Appointment Model
# -------------------------
class Appointment(Base):
    __tablename__ = "Appointment"

    AppointmentId = Column(Integer, primary_key=True, index=True)
    AppointmentNo = Column(String, nullable=True)

    LabId = Column(Integer, nullable=False)
    PatientName = Column(String, nullable=True)
    PatientAge = Column(Integer, nullable=True)
    PatientGender = Column(String, nullable=True)
    ContactNumber = Column(String, nullable=True)
    Email = Column(String, nullable=True)
    Address = Column(String, nullable=True)
    GPSLocation = Column(String, nullable=True)

    AppointmentDate = Column(Date, nullable=True)
    TimeSlot = Column(String, nullable=True)
    SelectedTests = Column(String, nullable=True)

    SampleCollectionMode = Column(String, nullable=True)
    TotalAmount = Column(Float, nullable=True, default=0.0)
    TotalGst = Column(Float, nullable=True, default=0.0)
    NetPayable = Column(Float, nullable=True, default=0.0)
    PaymentMethod = Column(String, nullable=True)
    PaymentStatus = Column(String, nullable=True)
    BookingStatus = Column(String, nullable=True)

    CreatedAt = Column(DateTime, default=ist_now)
    UpdatedAt = Column(DateTime, default=ist_now)
