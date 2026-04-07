from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from ...utils.timezone import ist_now
from .sql_base import Base


# -------------------------------------------------
# Service Provider Model
# -------------------------------------------------
class ServiceProvider(Base):
    __tablename__ = "ServiceProvider"

    ServiceProviderId = Column(Integer, primary_key=True, index=True)
    ProviderName = Column(String, nullable=False)

    PhotoUrl = Column(String, nullable=True)
    CertificateUrl = Column(String, nullable=True)
    AadhaarOrIdProofUrl = Column(String, nullable=True)

    Address = Column(String, nullable=False)
    Pincode = Column(String, nullable=False)

    PhoneNumber = Column(String, nullable=False)
    Email = Column(String, nullable=False)
    Password = Column(String, nullable=True)

    ExperienceYears = Column(Integer, nullable=False)
    Gender = Column(String, nullable=False)
    DateOfBirth = Column(String, nullable=False)
    LicenseNumber = Column(String, nullable=True)

    AvailabilityStatus = Column(String, nullable=True, default="available")  # available / unavailable / busy
    Rating = Column(Float, nullable=True, default=0.0)
    IsVerified = Column(Boolean, nullable=True, default=False)
    IsActive = Column(Boolean, nullable=True, default=True)

    Specialization = Column(String, nullable=False)
    ServiceDescription = Column(String, nullable=False)
    ServicesOffered = Column(Text, nullable=True)  # JSON string of services

    # Foreign Keys

    CreatedAt = Column(DateTime, default=ist_now)
    UpdatedAt = Column(DateTime, default=ist_now)

    # Relationships
    # One Service Provider → Many Service Requests
    service_requests = relationship(
        "ServiceRequest",
        foreign_keys="ServiceRequest.ServiceProviderId"
    )
