from pydantic import BaseModel
from typing import Optional, List


class ProviderServicesBase(BaseModel):
    ServiceProviderId: Optional[int] = None
    ServiceListId: Optional[int] = None
    Price: Optional[float] = None
    DurationMinutes: Optional[int] = None

    class Config:
        from_attributes = True


class ProviderServicesCreate(ProviderServicesBase):
    ServiceProviderId: int
    ServiceListId: int


class ProviderServicesBulkCreate(BaseModel):
    ServiceProviderId: int
    Services: List[ProviderServicesBase]   # multiple 


class ProviderServicesUpdate(ProviderServicesBase):
    pass


class ProviderServicesRead(ProviderServicesBase):
    ProviderServiceId: int