from pydantic import BaseModel
from typing import Optional
from datetime import date


class CustomerBase(BaseModel):
    FullName: Optional[str]
    ProfilePicture: Optional[str]
    DateOfBirth: Optional[date]
    Gender: Optional[str]
    Email: Optional[str]
    PhoneNumber: Optional[str]
    AddressLine1: str
    AddressLine2: Optional[str]
    City: str
    State: str
    Country: str
    PostalCode: str
    Latitude: Optional[float]
    Longitude: Optional[float]

    BankName: Optional[str]
    AccountNumber: Optional[str]
    IFSCCode: Optional[str]
    Branch: Optional[str]

    class Config:
        from_attributes = True


class CustomerCreate(CustomerBase):
    Email: str
    Password: str      # Plain password input


class CustomerUpdate(CustomerBase):
    # Password: Optional[str]
    pass


class CustomerRead(CustomerBase):
    CustomerId: int



