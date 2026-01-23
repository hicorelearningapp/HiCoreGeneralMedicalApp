from pydantic import BaseModel, Field
from datetime import datetime
from ...utils.timezone import ist_now
from typing import Optional

class PrescriptionBase(BaseModel):
    CustomerId: Optional[int]
    OrderId: Optional[int]
    DoctorName: Optional[str]
    DocumentUrl: Optional[str]
    Status: Optional[str]
    Verified: Optional[bool] = False
    VerifiedBy: Optional[str]
    UploadedAt: Optional[datetime] = Field(default_factory=ist_now)

    class Config:
        from_attributes = True

class PrescriptionCreate(PrescriptionBase):
    CustomerId: int
    OrderId: int
    DocumentUrl: str

class PrescriptionUpdate(BaseModel):
    Verified: Optional[bool]
    VerifiedBy: Optional[str]

class PrescriptionRead(PrescriptionBase):
    PrescriptionId: int
