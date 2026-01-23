from sqlalchemy import Column, Integer, String
from .sql_base import Base

class Pharmacy(Base):
    __tablename__ = "Pharmacy"

    PharmacyId = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)
    Address = Column(String, nullable=True)
    GPSLocation = Column(String, nullable=True)  # "lat,lon" format
    Pincode = Column(String, nullable=True)
    ImgUrl = Column(String, nullable=True)
    Contact = Column(String, nullable=True)
    Email = Column(String, nullable=True)
