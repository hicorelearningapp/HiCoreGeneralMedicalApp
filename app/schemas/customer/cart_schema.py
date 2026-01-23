from pydantic import BaseModel
from typing import Optional, List


class AddToCart(BaseModel):
    CustomerId: int
    MedicineId: int
    Quantity: int


class UpdateCartItem(BaseModel):
    Quantity: Optional[int]


class CartItemDetail(BaseModel):
    MedicineId: int
    Name: Optional[str]
    ImgUrl: Optional[str]

    OldPrice: float
    NewPrice: float
    PriceChanged: bool

    Quantity: int
    Amount: float


class CartResponse(BaseModel):
    CartId: Optional[int]
    CustomerId: int
    Items: List[CartItemDetail]
    TotalAmount: float
