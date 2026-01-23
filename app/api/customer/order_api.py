from fastapi import APIRouter, HTTPException
from typing import List
from ...crud.customer.order_manager import OrderManager, OrderItemManager
from ...schemas.customer.order_schema import OrderCreate, OrderItemCreate
from ...schemas.customer.order_schema import OrderItemCreate, OrderItemUpdate
from ...config import settings


class OrderAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = OrderManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.get("/orders/customer/{customer_id}")(self.get_orders_by_customer)
        self.router.get("/orders/retailer/{retailer_id}")(self.get_orders_by_retailer)
        self.router.post("/customer/orders")(self.create_order)
        self.router.get("/customer/orders/{order_id}")(self.get_order)
        self.router.put("/customer/orders/{order_id}")(self.update_order)
        self.router.delete("/customer/orders/{order_id}")(self.delete_order)

    async def create_order(self, order: OrderCreate, items: List[OrderItemCreate]):
        return await self.crud.create_order(order, items)

    async def get_order(self, order_id: int):
        return await self.crud.get_order(order_id)

    async def update_order(self, order_id: int, data: dict):
        return await self.crud.update_order(order_id, data)

    async def delete_order(self, order_id: int):
        return await self.crud.delete_order(order_id)

    async def get_orders_by_customer(self, customer_id: int):
        return await self.crud.get_orders_by_customer(customer_id)

    async def get_orders_by_retailer(self, retailer_id: int):
        return await self.crud.get_orders_by_retailer(retailer_id)




class OrderItemAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = OrderItemManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/customer/order-items")(self.create_order_item)
        self.router.get("/customer/order-items/{item_id}")(self.get_order_item)
        self.router.get("/customer/order-items/by-order/{order_id}")(self.get_items_by_order)
        self.router.put("/customer/order-items/{item_id}")(self.update_order_item)
        self.router.delete("/customer/order-items/{item_id}")(self.delete_order_item)

    # ---------------------------------------------------------
    # Create Order Item
    # ---------------------------------------------------------
    async def create_order_item(self, item: OrderItemCreate):
        result = await self.crud.create_order_item(item)
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["message"])
        return result

    # ---------------------------------------------------------
    # Get Order Item
    # ---------------------------------------------------------
    async def get_order_item(self, item_id: int):
        result = await self.crud.get_order_item(item_id)
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["message"])
        return result

    # ---------------------------------------------------------
    # Get Items by OrderId
    # ---------------------------------------------------------
    async def get_items_by_order(self, order_id: int):
        result = await self.crud.get_items_by_order(order_id)
        return result

    # ---------------------------------------------------------
    # Update Order Item
    # ---------------------------------------------------------
    async def update_order_item(self, item_id: int, item: OrderItemUpdate):
        result = await self.crud.update_order_item(item_id, item)
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["message"])
        return result

    # ---------------------------------------------------------
    # Delete Order Item
    # ---------------------------------------------------------
    async def delete_order_item(self, item_id: int):
        result = await self.crud.delete_order_item(item_id)
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["message"])
        return result
