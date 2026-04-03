from sqlalchemy import Column, Integer, String, Float
from .sql_base import Base


# -------------------------------------------------
# Doctor Service Model
# -------------------------------------------------
class DoctorService(Base):
    __tablename__ = "DoctorService"

    DoctorServiceId = Column(Integer, primary_key=True, index=True)
    Service = Column(String, nullable=False)
    Amount = Column(Float, nullable=False)