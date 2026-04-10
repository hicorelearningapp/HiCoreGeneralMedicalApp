from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class CustomerBase(BaseModel):
    FullName: Optional[str] = None
    ProfilePicture: Optional[str] = None
    DateOfBirth: Optional[date] = None
    Gender: Optional[str] = None
    Email: Optional[str] = None
    PhoneNumber: Optional[str] = None
    AddressLine1: Optional[str] = None
    AddressLine2: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Country: Optional[str] = None
    PostalCode: Optional[str] = None
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None

    BankName: Optional[str] = None
    AccountNumber: Optional[str] = None
    IFSCCode: Optional[str] = None
    Branch: Optional[str] = None

    class Config:
        from_attributes = True


class CustomerCreate(CustomerBase):
    Email: Optional[str]
    Password: Optional[str]      # Plain password input


class CustomerUpdate(CustomerBase):
    Password: Optional[str] = None


class CustomerRead(CustomerBase):
    CustomerId: int
    # PasswordHash: Optional[str]



class RegisterSchema(BaseModel):
    Email: Optional[str]
    Password: Optional[str]


class LoginSchema(BaseModel):
    Email: Optional[str]
    Password: Optional[str]
