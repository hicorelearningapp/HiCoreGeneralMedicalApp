from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from ...utils.timezone import ist_now
from .sql_base import Base


class Order(Base):
    __tablename__ = "Orders"

    OrderId = Column(Integer, primary_key=True, index=True)
    CustomerId = Column(Integer, nullable=False)
    RetailerId = Column(Integer, nullable=False)
    RetailerName = Column(String, nullable=False)

    OrderDateTime = Column(DateTime, default=ist_now)
    ExpectedDelivery = Column(DateTime, nullable=True)

    # Delivery info
    DeliveryMode = Column(String, nullable=True)
    DeliveryService = Column(String, nullable=True)
    DeliveryPartnerTrackingId = Column(String, nullable=True)
    DeliveryStatus = Column(String, default="Pending")  # Pending, Shipped, Delivered

    # Payment info
    PaymentMode = Column(String, nullable=True)
    PaymentStatus = Column(String, default="Pending")  # Pending, Paid, Failed    
    
    # Prescription info
    PrescriptionFileUrl = Column(String, nullable=True)
    PrescriptionVerified = Column(Boolean, default=False)

 
    TotalAmount = Column(Float, default=0.0)  # Total order amount including GST
    Status = Column(String, default="New")  # Pending, Cancelled, Completed

    # Audit fields
    CreatedAt = Column(DateTime, default=ist_now)
    UpdatedAt = Column(DateTime, default=ist_now, onupdate=ist_now)


class OrderItem(Base):
    __tablename__ = "OrderItem"

    OrderItemId = Column(Integer, primary_key=True, index=True)
    OrderId = Column(Integer, nullable=False)
    CustomerId = Column(Integer, nullable=False)
    RetailerId = Column(Integer, nullable=False)

    MedicineId = Column(Integer, nullable=False)
    MedicineName = Column(String, nullable=False)
    Quantity = Column(Integer, nullable=False)

    Price = Column(Float, nullable=False)    

    TotalAmount = Column(Float, nullable=False)      # (UnitPrice * Quantity) + GST
