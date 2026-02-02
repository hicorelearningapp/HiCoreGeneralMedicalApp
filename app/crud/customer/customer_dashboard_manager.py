from typing import Dict
from datetime import datetime
from ...db.base.database_manager import DatabaseManager
from ...models.customer.order_model import Order
from ...models.customer.customer_model import Customer


class CustomerDashboardManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def get_dashboard(self, customer_id: int) -> Dict:
        await self.db_manager.connect()

        try:
            # Fetch all orders for the customer
            orders = await self.db_manager.read(
                Order, {"CustomerId": customer_id}
            )

            # Initialize counters
            total_orders = len(orders)
            active_orders = 0
            pending = 0
            cancelled = 0
            delivered = 0

            # Count orders by status
            for o in orders:
                if o.Status == "Cancelled":
                    cancelled += 1
                elif o.Status in ("New", "Pending"):
                    pending += 1
                elif o.Status == "InTransit":
                    active_orders += 1
                elif o.Status == "Delivered":
                    delivered += 1

            # Fetch customers
            # customers = await self.db_manager.read(Customer, {})
            # customer_map = {c.CustomerId: c.FullName for c in customers}

            return {
                "TotalOrders": total_orders,
                "ActiveOrders": active_orders,
                "Pending": pending,
                "Cancelled": cancelled,
                "Delivered": delivered,
                "RecentOrders": [
                    {
                        "OrderID": o.OrderId,
                        "RetailerName": o.RetailerName,
                        "Price": o.TotalAmount,
                        "Status": o.Status,
                        "OrderDateTime": o.OrderDateTime
                    }
                    for o in orders
                ]
            }

        finally:
            await self.db_manager.disconnect()
