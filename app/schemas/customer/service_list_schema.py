from pydantic import BaseModel
from typing import Optional


class ServiceListBase(BaseModel):
    ServiceName: Optional[str] = None
    Description: Optional[str] = None

    class Config:
        from_attributes = True


class ServiceListCreate(ServiceListBase):
    ServiceName: str   # required for create


class ServiceListUpdate(ServiceListBase):
    pass


class ServiceListRead(ServiceListBase):
    ServiceListId: int