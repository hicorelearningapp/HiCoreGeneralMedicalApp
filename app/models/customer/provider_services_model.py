from sqlalchemy import Column, Integer, Float, ForeignKey
from .sql_base import Base


class ProviderServices(Base):
    __tablename__ = "providerservices"

    ProviderServiceId = Column(Integer, primary_key=True, index=True)

    ServiceProviderId = Column(Integer, ForeignKey("serviceprovider.ServiceProviderId"))
    ServiceListId = Column(Integer, ForeignKey("servicelist.ServiceListId"))

    Price = Column(Float, nullable=True)
    DurationMinutes = Column(Integer, nullable=True)