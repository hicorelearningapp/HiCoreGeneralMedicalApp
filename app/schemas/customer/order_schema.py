from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from ...utils.timezone import ist_now


# ----------------- OrderItem Schemas -----------------
class OrderItemBase(BaseModel):
    OrderId: Optional[int]
    CustomerId: Optional[int]
    RetailerId: Optional[int]
    MedicineId: int
    Quantity: int
    GSTPercentage: float   
    TotalAmount: float  # (Price * Quantity) + GST, handled in manager


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    OrderItemId: int

    class Config:
        from_attributes = True


# ----------------- Order Schemas -----------------
class OrderBase(BaseModel):
    CustomerId: Optional[int]
    RetailerId: Optional[int]
    
    OrderDateTime: Optional[datetime] = Field(default_factory=ist_now)
    ExpectedDelivery: Optional[datetime] = Field(default_factory=ist_now)

    DeliveryMode: Optional[str]
    DeliveryService: Optional[str]
    DeliveryPartnerTrackingId: Optional[str]
    DeliveryStatus: Optional[str] = "Pending"

    PaymentMode: Optional[str]
    PaymentStatus: Optional[str] = "Pending"
    Amount: Optional[float] = 0.0
    
    PrescriptionFileUrl: Optional[str]
    PrescriptionVerified: Optional[bool] = False

    OrderStatus: Optional[str] = "Pending"

    CreatedAt: Optional[datetime] = Field(default_factory=ist_now)
    UpdatedAt: Optional[datetime] = Field(default_factory=ist_now)


class OrderCreate(OrderBase):
    CustomerId: int
    RetailerId: int
    Amount: float
    # You can optionally include order items
    # Items: Optional[List[OrderItemCreate]] = []


class OrderUpdate(OrderBase):
    pass


class OrderRead(OrderBase):
    OrderId: int
    Items: Optional[List[OrderItemRead]] = []

    class Config:
        from_attributes = True
