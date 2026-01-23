from sqlalchemy import Column, Integer, String, Boolean, DateTime
from ...utils.timezone import ist_now
from .sql_base import Base

class Prescription(Base):
    __tablename__ = "Prescription"

    PrescriptionId = Column(Integer, primary_key=True, index=True)
    CustomerId = Column(Integer, nullable=False)
    OrderId = Column(Integer, nullable=False)
    DoctorName = Column(String, nullable=True)
    DocumentUrl = Column(String, nullable=False)
    Status = Column(String, default="Pending")   # Pending, Cancelled, Completed, Processing
    Verified = Column(Boolean, default=False)
    VerifiedBy = Column(String, nullable=True)
    UploadedAt = Column(DateTime, default=ist_now)
