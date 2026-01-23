from sqlalchemy import (
    Column, Integer, String, Boolean, Date, Float, UniqueConstraint
)
from .sql_base import Base


# -------------------------------
#   CUSTOMER MODEL
# -------------------------------
class Customer(Base):
    __tablename__ = "customer"

    CustomerId = Column(Integer, primary_key=True, index=True)

    FullName = Column(String(255), nullable=True)
    ProfilePicture = Column(String(255), nullable=True)

    DateOfBirth = Column(Date, nullable=True)
    Gender = Column(String(50), nullable=True)

    Email = Column(String(255), nullable=False, unique=True)
    PasswordHash = Column(String(255), nullable=False)

    PhoneNumber = Column(String(20), nullable=True)

    AddressLine1 = Column(String(255), nullable=False)
    AddressLine2 = Column(String(255), nullable=True)
    City = Column(String(100), nullable=False)
    State = Column(String(100), nullable=False)
    Country = Column(String(100), nullable=False)
    PostalCode = Column(String(20), nullable=False)

    Latitude = Column(Float, nullable=True)
    Longitude = Column(Float, nullable=True)

    BankName = Column(String(255), nullable=True)
    AccountNumber = Column(String(50), nullable=True)
    IFSCCode = Column(String(50), nullable=True)
    Branch = Column(String(255), nullable=True)

