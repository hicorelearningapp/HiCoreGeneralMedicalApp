from fastapi import APIRouter
from typing import Optional
from ...config import settings
from ...schemas.customer.order_schema import (
    OrderCreate,
    OrderUpdate,
)
from ...crud.customer.order_manager import OrderManager
from ...schemas.customer.order_schema import (
    OrderItemCreate,
    OrderItemUpdate,
)
from ...crud.customer.order_manager import OrderItemManager



class OrderAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = OrderManager(settings.db_type)
        self.register()

    def register(self):
        self.router.post("/orders")(self.create)
        self.router.get("/orders/{order_id}")(self.get)
        self.router.get("/orders/customer/{customer_id}")(self.get_by_customer)
        self.router.get("/orders/retailer/{retailer_id}")(self.get_by_retailer)
        self.router.put("/orders/{order_id}")(self.update)
        self.router.patch("/orders/{order_id}/status")(self.update_status)
        self.router.delete("/orders/{order_id}")(self.delete)

    async def create(self, data: OrderCreate):
        return await self.manager.create_order(data)

    async def get(self, order_id: int):
        return await self.manager.get_order(order_id)

    async def get_by_customer(self, customer_id: Optional[int] = None):
        return await self.manager.get_orders_by_customer(customer_id)

    async def get_by_retailer(self, retailer_id: Optional[int] = None):
        return await self.manager.get_orders_by_retailer(retailer_id)

    async def update(self, order_id: int, data: OrderUpdate):
        return await self.manager.update_order(order_id, data)
    
    async def update_status(self, order_id: int, status: str):
        return await self.manager.update_order_status(order_id, status)


    async def delete(self, order_id: int):
        return await self.manager.delete_order(order_id)




class OrderItemAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = OrderItemManager(settings.db_type)
        self.register()

    def register(self):
        self.router.post("/order-items")(self.create)
        self.router.get("/order-items/order/{order_id}")(self.get_by_order)
        self.router.put("/order-items/{item_id}")(self.update)
        self.router.delete("/order-items/{item_id}")(self.delete)

    async def create(self, data: OrderItemCreate):
        return await self.manager.create_item(data)

    async def get_by_order(self, order_id: int):
        return await self.manager.get_items_by_order(order_id)

    async def update(self, item_id: int, data: OrderItemUpdate):
        return await self.manager.update_item(item_id, data)

    async def delete(self, item_id: int):
        return await self.manager.delete_item(item_id)
