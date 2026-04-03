from typing import Optional
from pydantic import BaseModel


# -------------------------------
# Doctor Service Schemas
# -------------------------------
class DoctorServiceBase(BaseModel):
    Service: Optional[str]
    Amount: Optional[float]

    class Config:
        from_attributes = True


class DoctorServiceCreate(DoctorServiceBase):
    Service: str
    Amount: float


class DoctorServiceUpdate(DoctorServiceBase):
    pass