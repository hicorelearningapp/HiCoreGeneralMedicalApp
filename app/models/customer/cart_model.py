from sqlalchemy import Column, Integer, Float, DateTime
from ...utils.timezone import ist_now
from .sql_base import Base


class Cart(Base):
    __tablename__ = "Cart"

    CartId = Column(Integer, primary_key=True, index=True)
    CustomerId = Column(Integer, nullable=False)
    CreatedAt = Column(DateTime, default=ist_now)


class CartItem(Base):
    __tablename__ = "CartItem"

    CartItemId = Column(Integer, primary_key=True, index=True)
    CartId = Column(Integer, nullable=False)
    MedicineId = Column(Integer, nullable=False)
    Quantity = Column(Integer, nullable=False)

    StoredPrice = Column(Float, nullable=False)
