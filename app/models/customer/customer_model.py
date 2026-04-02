from sqlalchemy import (
    Column, Integer, String, Boolean, Date, Float, UniqueConstraint, ForeignKey
)
from sqlalchemy.orm import relationship
from .sql_base import Base


# -------------------------------
#   CUSTOMER MODEL
# -------------------------------
class Customer(Base):
    __tablename__ = "customer"

    CustomerId = Column(Integer, primary_key=True, index=True)

    CustomerName = Column(String(255), nullable=False)
    ProfilePicture = Column(String(500), nullable=True)

    DateOfBirth = Column(Date, nullable=True)
    Gender = Column(String(20), nullable=True)

    Email = Column(String(255), nullable=False, unique=True)
    PasswordHash = Column(String(255), nullable=True)

    CustomerPhoneNumber = Column(String(20), nullable=True)

    AddressLine1 = Column(String(255), nullable=True)
    AddressLine2 = Column(String(255), nullable=True)
    City = Column(String(100), nullable=True)
    State = Column(String(100), nullable=True)
    Country = Column(String(100), nullable=True)
    PostalCode = Column(String(20), nullable=True)

    Latitude = Column(Float, nullable=True)
    Longitude = Column(Float, nullable=True)

    BankName = Column(String(255), nullable=True)
    AccountNumber = Column(String(50), nullable=True)
    IFSCCode = Column(String(50), nullable=True)
    Branch = Column(String(255), nullable=True)

    # Relationships
    # One Customer → Many Service Requests
    service_requests = relationship(
        "ServiceRequest",
        foreign_keys="ServiceRequest.CustomerId"
    )

