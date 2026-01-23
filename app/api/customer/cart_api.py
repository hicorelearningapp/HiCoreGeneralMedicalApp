from fastapi import APIRouter, HTTPException
from ...crud.customer.cart_manager import CartManager
from ...schemas.customer.cart_schema import AddToCart, UpdateCartItem
from ...config import settings


class CartAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = CartManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/cart")(self.add_to_cart)
        self.router.get("/cart/{customer_id}")(self.get_cart)
        self.router.put("/cart/item/{cart_item_id}")(self.update_item)
        self.router.delete("/cart/item/{cart_item_id}")(self.delete_item)
        self.router.delete("/cart/clear/{customer_id}")(self.clear_cart)

    async def add_to_cart(self, data: AddToCart):
        return await self.crud.add_to_cart(data)

    async def get_cart(self, customer_id: int):
        return await self.crud.get_cart(customer_id)

    async def update_item(self, cart_item_id: int, data: UpdateCartItem):
        return await self.crud.update_item(cart_item_id, data)

    async def delete_item(self, cart_item_id: int):
        return await self.crud.delete_item(cart_item_id)

    async def clear_cart(self, customer_id: int):
        return await self.crud.clear_cart(customer_id)
