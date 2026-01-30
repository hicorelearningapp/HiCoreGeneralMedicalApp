from typing import Optional, Dict, Any
from ...utils.timezone import ist_now
from ...utils.logger import get_logger
from ...db.base.database_manager import DatabaseManager

from ...models.customer.order_model import Order, OrderItem
from ...models.customer.customer_model import Customer
from ...schemas.customer.order_schema import (
    OrderCreate,
    OrderUpdate,
    OrderRead,
    OrderItemCreate,
    OrderItemRead,
)
from ...models.customer.order_model import Order, OrderItem
from ...schemas.customer.order_schema import (
    OrderItemCreate,
    OrderItemUpdate,
    OrderItemRead,
)


logger = get_logger(__name__)


class OrderManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    # ------------------------------------------------------------
    # 🟢 Create Order + Items
    # ------------------------------------------------------------
    async def create_order(self, order: OrderCreate) -> dict:
        try:
            await self.db_manager.connect()

            order_data = order.dict(exclude={"Items"})
            order_data["OrderDateTime"] = ist_now()

            new_order = await self.db_manager.create(Order, order_data)
            order_id = new_order.OrderId

            total_amount = 0.0

            # ---- Create items ----
            if order.Items:
                for item in order.Items:
                    item_data = item.dict()
                    item_data["OrderId"] = order_id
                    item_data["TotalAmount"] = (item.Price or 0) * (item.Quantity or 0)

                    total_amount += item_data["TotalAmount"]

                    await self.db_manager.create(OrderItem, item_data)

            # ---- Update totals ----
            await self.db_manager.update(
                Order,
                {"OrderId": order_id},
                {
                    "TotalAmount": total_amount,
                    "UpdatedAt": ist_now(),
                },
            )

            logger.info(f"✅ Order {order_id} created with items")

            return {
                "success": True,
                "message": "Order created successfully",
                "OrderId": order_id,
            }

        except Exception as e:
            logger.error(f"❌ Error creating order: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db_manager.disconnect()

    # ------------------------------------------------------------
    # 🟡 Get Order + Items (SAME OUTPUT)
    # ------------------------------------------------------------
    async def get_order(self, order_id: int) -> dict:
        try:
            await self.db_manager.connect()

            orders = await self.db_manager.read(Order, {"OrderId": order_id})
            if not orders:
                return {"success": False, "message": "Order not found"}

            order = orders[0]

            items = await self.db_manager.read(
                OrderItem, {"OrderId": order_id}
            )

            order_schema = OrderRead.from_orm(order).dict()
            order_schema["Customer"] = await self.db_manager.read(
                Customer, {"CustomerId": order.CustomerId}
            )
            order_schema["Items"] = [item.__dict__ for item in items]

            return order_schema

        except Exception as e:
            logger.error(f"❌ Error fetching order {order_id}: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db_manager.disconnect()

    # ------------------------------------------------------------
    # 🟢 Get Orders by Customer (SAME COUNTS)
    # ------------------------------------------------------------
    async def get_orders_by_customer(self, customer_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            await self.db_manager.connect()

            query = {"CustomerId": customer_id} if customer_id else None
            result = await self.db_manager.read(Order, query)

            orders = [OrderRead.from_orm(o).dict() for o in result]

            total_orders = len(orders)

            delivered = sum(1 for o in orders if o.get("Status") == "Delivered")
            in_transit = sum(1 for o in orders if o.get("Status") == "InTransit")
            placed = sum(
                1 for o in orders
                if o.get("Status") in ("New", "Pending")
            )

            return {
                "TotalOrders": total_orders,
                "Delivered": delivered,
                "InTransit": in_transit,
                "Placed": placed,
                "Data": orders
            }

        except Exception as e:
            logger.error(f"❌ Error fetching customer orders: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db_manager.disconnect()

    # ------------------------------------------------------------
    # 🟢 Get Orders by Retailer (SAME COUNTS + NewOrders)
    # ------------------------------------------------------------
    async def get_orders_by_retailer(self, retailer_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            await self.db_manager.connect()

            query = {"RetailerId": retailer_id} if retailer_id else None
            result = await self.db_manager.read(Order, query)

            orders = [OrderRead.from_orm(o).dict() for o in result]

            new_orders = [
                await self.get_order(o.get("OrderId"))
                for o in orders
                if o.get("Status") == "New"
            ]

            total_orders = len(orders)

            delivered = sum(1 for o in orders if o.get("Status") == "Delivered")
            cancelled = sum(1 for o in orders if o.get("Status") == "Cancelled")
            in_transit = sum(1 for o in orders if o.get("Status") == "InTransit")
            pending = sum(1 for o in orders if o.get("Status") == "Pending")
            new = sum(1 for o in orders if o.get("Status") == "New")
            accepted = sum(
                1 for o in orders
                if o.get("Status") not in ("New", "Cancelled")
            )

            return {
                "TotalOrders": total_orders,
                "New": new,
                "Accepted": accepted,
                "Pending": pending,
                "InTransit": in_transit,
                "Delivered": delivered,
                "Cancelled": cancelled,
                "NewOrders": new_orders,
                "AllOrders": orders
            }

        except Exception as e:
            logger.error(f"❌ Error fetching retailer orders: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db_manager.disconnect()

    # ------------------------------------------------------------
    # 🟠 Update Order
    # ------------------------------------------------------------
    async def update_order(self, order_id: int, data: OrderUpdate) -> dict:
        try:
            await self.db_manager.connect()

            rowcount = await self.db_manager.update(
                Order,
                {"OrderId": order_id},
                data.dict(exclude_unset=True),
            )

            if rowcount:
                return {"success": True, "message": "Order updated"}

            return {"success": False, "message": "Order not found"}

        except Exception as e:
            logger.error(f"❌ Error updating order: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db_manager.disconnect()

    
    # ------------------------------------------------------------
    # 🔵 Update Order Status ONLY
    # ------------------------------------------------------------
    async def update_order_status(self, order_id: int, status: str) -> dict:
        try:
            await self.db_manager.connect()

            # Optional: enforce allowed status transitions
            # allowed_status = {"New", "Pending", "InTransit", "Delivered", "Cancelled"}
            # if status not in allowed_status:
            #     return {"success": False, "message": "Invalid status value"}

            rowcount = await self.db_manager.update(
                Order,
                {"OrderId": order_id},
                {
                    "Status": status,
                    "UpdatedAt": ist_now()
                }
            )

            if rowcount:
                return {
                    "success": True,
                    "message": f"Order status updated to {status}"
                }

            return {"success": False, "message": "Order not found"}

        except Exception as e:
            logger.error(f"❌ Error updating order status: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db_manager.disconnect()


    # ------------------------------------------------------------
    # 🔴 Delete Order + Items
    # ------------------------------------------------------------
    async def delete_order(self, order_id: int) -> dict:
        try:
            await self.db_manager.connect()

            await self.db_manager.delete(
                OrderItem, {"OrderId": order_id}
            )

            rowcount = await self.db_manager.delete(
                Order, {"OrderId": order_id}
            )

            if rowcount:
                return {"success": True, "message": "Order deleted"}

            return {"success": False, "message": "Order not found"}

        except Exception as e:
            logger.error(f"❌ Error deleting order: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db_manager.disconnect()




class OrderItemManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    # ------------------------------------------------------------
    # 🟢 Create Item
    # ------------------------------------------------------------
    async def create_item(self, item: OrderItemCreate) -> dict:
        try:
            await self.db_manager.connect()

            data = item.dict()
            data["TotalAmount"] = (item.Price or 0) * (item.Quantity or 0)

            new_item = await self.db_manager.create(OrderItem, data)

            # ---- Update order total ----
            items = await self.db_manager.read(
                OrderItem, {"OrderId": item.OrderId}
            )

            total_amount = sum(i.TotalAmount for i in items)

            await self.db_manager.update(
                Order,
                {"OrderId": item.OrderId},
                {
                    "TotalAmount": total_amount,
                    "UpdatedAt": ist_now()
                }
            )

            return {
                "success": True,
                "OrderItemId": new_item.OrderItemId
            }

        except Exception as e:
            logger.error(f"❌ Create order item failed: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db_manager.disconnect()

    # ------------------------------------------------------------
    # 🟡 Get Items by Order
    # ------------------------------------------------------------
    async def get_items_by_order(self, order_id: int):
        try:
            await self.db_manager.connect()

            items = await self.db_manager.read(
                OrderItem, {"OrderId": order_id}
            )

            return [
                OrderItemRead.from_orm(i).dict()
                for i in items
            ]

        except Exception as e:
            logger.error(f"❌ Fetch order items failed: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db_manager.disconnect()

    # ------------------------------------------------------------
    # 🟠 Update Item
    # ------------------------------------------------------------
    async def update_item(self, item_id: int, data: OrderItemUpdate):
        try:
            await self.db_manager.connect()

            count = await self.db_manager.update(
                OrderItem,
                {"OrderItemId": item_id},
                data.dict(exclude_unset=True)
            )

            if count:
                return {"success": True, "message": "Order item updated"}

            return {"success": False, "message": "Order item not found"}

        except Exception as e:
            logger.error(f"❌ Update order item failed: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db_manager.disconnect()

    # ------------------------------------------------------------
    # 🔴 Delete Item
    # ------------------------------------------------------------
    async def delete_item(self, item_id: int):
        try:
            await self.db_manager.connect()

            item = await self.db_manager.read(
                OrderItem, {"OrderItemId": item_id}
            )
            if not item:
                return {"success": False, "message": "Order item not found"}

            order_id = item[0].OrderId

            await self.db_manager.delete(
                OrderItem, {"OrderItemId": item_id}
            )

            # ---- Recalculate order total ----
            items = await self.db_manager.read(
                OrderItem, {"OrderId": order_id}
            )

            total_amount = sum(i.TotalAmount for i in items)

            await self.db_manager.update(
                Order,
                {"OrderId": order_id},
                {
                    "TotalAmount": total_amount,
                    "UpdatedAt": ist_now()
                }
            )

            return {"success": True, "message": "Order item deleted"}

        except Exception as e:
            logger.error(f"❌ Delete order item failed: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db_manager.disconnect()
