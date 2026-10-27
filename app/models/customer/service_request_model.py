from sqlalchemy import Column, Integer, String, Date, Time, Float, DateTime
from datetime import datetime
from .sql_base import Base


class ServiceRequest(Base):
    __tablename__ = "servicerequest"

    ServiceRequestId = Column(Integer, primary_key=True, index=True)

    CustomerId = Column(Integer, nullable=True)
    ServiceProviderId = Column(Integer, nullable=True)

    ServiceListId = Column(Integer, nullable=True)
    ProviderServiceId = Column(Integer, nullable=True)

    CustomerName = Column(String(255), nullable=True)
    CustomerPhone = Column(String(20), nullable=True)
    CustomerAddress = Column(String(500), nullable=True)
    Pincode = Column(String(20), nullable=True)

    PreferredDate = Column(Date, nullable=True)
    PreferredStartTime = Column(String(20), nullable=True)
    PreferredEndTime = Column(String(20), nullable=True)

    RequestDescription = Column(String(1000), nullable=True)

    Status = Column(String(50), default="pending")

    FinalPrice = Column(Float, nullable=True)
    AssignmentMode = Column(String(50), nullable=True)
    NotificationPreference = Column(String(50), nullable=True)

    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)