from pydantic import BaseModel, Field
from datetime import datetime
from ...utils.timezone import ist_now
from typing import Optional


class CustomerNotificationBase(BaseModel):
    CustomerId: Optional[int]
    Title: Optional[str]
    Message: Optional[str]
    Type: Optional[str]
    IsRead: Optional[bool] = False
    Date: Optional[datetime] = Field(default_factory=ist_now)

    class Config:
        from_attributes = True


class CustomerNotificationCreate(CustomerNotificationBase):
    CustomerId: int
    Title: str
    Message: str
    Type: str


class CustomerNotificationUpdate(BaseModel):
    IsRead: Optional[bool]


class CustomerNotificationRead(CustomerNotificationBase):
    NotificationId: int
