from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ...utils.timezone import ist_now
from .sql_base import Base


# -------------------------------------------------
# Service Request Model
# -------------------------------------------------
class ServiceRequest(Base):
    __tablename__ = "ServiceRequest"

    RequestId = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    CustomerId = Column(Integer, ForeignKey("customer.CustomerId"), nullable=False)
    ServiceProviderId = Column(Integer, ForeignKey("ServiceProvider.ServiceProviderId"), nullable=True)
    
    ServiceName = Column(String, nullable=True)

    CustomerName = Column(String, nullable=False)
    CustomerPhone = Column(String, nullable=False)
    CustomerAddress = Column(Text, nullable=False)

    PreferredDate = Column(Date, nullable=True)
    PreferredTime = Column(String, nullable=True)
    RequestDescription = Column(Text, nullable=True)
    Pincode = Column(String, nullable=True)

    Status = Column(String, nullable=False, default="pending")  # pending, assigned, accepted, in_progress, completed, cancelled, rejected

    AssignedAt = Column(DateTime, nullable=True)
    AcceptedAt = Column(DateTime, nullable=True)
    CompletedAt = Column(DateTime, nullable=True)
    CancelledAt = Column(DateTime, nullable=True)

    CustomerNotes = Column(Text, nullable=True)
    ProviderNotes = Column(Text, nullable=True)

    EstimatedPrice = Column(Float, nullable=True)
    FinalPrice = Column(Float, nullable=True)
    PaymentStatus = Column(String, nullable=True, default="pending")  # pending, paid, failed

    AssignmentMode = Column(String, nullable=True, default="random")  # random, visible_profile

    NotificationPreference = Column(String, nullable=True, default="both")  # whatsapp, sms, both

    CreatedAt = Column(DateTime, default=ist_now)
    UpdatedAt = Column(DateTime, default=ist_now)

    # Relationships
    # Belongs to one Customer
    customer = relationship(
        "Customer",
        foreign_keys=[CustomerId]
    )
    
    # Belongs to one Service Provider (nullable initially)
    service_provider = relationship(
        "ServiceProvider",
        foreign_keys=[ServiceProviderId]
    )
