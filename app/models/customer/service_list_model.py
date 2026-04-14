from sqlalchemy import Column, Integer, String
from .sql_base import Base


class ServiceList(Base):
    __tablename__ = "servicelist"

    ServiceListId = Column(Integer, primary_key=True, index=True)
    ServiceName = Column(String(255), nullable=False)
    Description = Column(String(1000), nullable=True)