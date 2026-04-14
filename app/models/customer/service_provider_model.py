from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from datetime import datetime
from .sql_base import Base


class ServiceProvider(Base):
    __tablename__ = "serviceprovider"

    ServiceProviderId = Column(Integer, primary_key=True, index=True)

    ProviderName = Column(String(255), nullable=True)
    PhotoUrl = Column(String(500), nullable=True)

    Address = Column(String(500), nullable=True)
    Pincode = Column(String(20), nullable=True)

    PhoneNumber = Column(String(20), nullable=True)
    Email = Column(String(255), nullable=False, unique=True)
    PasswordHash = Column(String(255), nullable=True)

    ExperienceYears = Column(Integer, nullable=True)
    Gender = Column(String(20), nullable=True)
    DateOfBirth = Column(Date, nullable=True)

    AvailabilityStatus = Column(String(50), nullable=True)
    Rating = Column(Float, nullable=True)

    Specialization = Column(String(255), nullable=True)
    ServiceDescription = Column(String(1000), nullable=True)

    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)