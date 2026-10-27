from pydantic import BaseModel
from typing import Optional


class ServiceListBase(BaseModel):
    ServiceName: Optional[str] = None
    Price: Optional[float] = None
    DurationMinutes: Optional[int] = None
    Description: Optional[str] = None

    class Config:
        from_attributes = True


class ServiceListCreate(ServiceListBase):
    ServiceName: str


class ServiceListUpdate(ServiceListBase):
    pass


class ServiceListRead(ServiceListBase):
    ServiceListId: int