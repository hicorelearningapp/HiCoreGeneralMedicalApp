from ...utils.timezone import ist_now
from ...db.base.database_manager import DatabaseManager
from ...models.customer.order_model import Order, OrderItem
# from ...models.retailer.retailer_model import Retailer
from ...models.customer.customer_model import Customer
from ...schemas.customer.order_schema import OrderCreate, OrderItemCreate

from ...models.customer.order_model import OrderItem
from ...schemas.customer.order_schema import OrderItemCreate, OrderItemUpdate

from ...utils.logger import get_logger

logger = get_logger(__name__)


class OrderManager:
    def __init__(self, db_type: str):
        self.db = DatabaseManager(db_type)

    # ------------------------
    # Create Order
    # ------------------------
    async def create_order(self, order_data: OrderCreate, items: list):
        try:
            await self.db.connect()

            # Calculate total order amount with GST included
            total_amount = 0
            for i in items:
                item_base_amount = i.UnitPrice * i.Quantity
                gst_amount = (item_base_amount * i.GSTPercentage) / 100
                total_amount += (item_base_amount + gst_amount)

            # Prepare order dictionary
            order_dict = order_data.dict()
            order_dict["Amount"] = total_amount
            order_dict["CreatedAt"] = ist_now()
            order_dict["UpdatedAt"] = ist_now()

            # Insert order
            order_obj = await self.db.create(Order, order_dict)
            order_id = order_obj.OrderId

            # Insert items
            for i in items:
                i_dict = i.dict()
                i_dict["OrderId"] = order_id

                base_amount = i.UnitPrice * i.Quantity
                gst_amount = (base_amount * i.GSTPercentage) / 100
                i_dict["TotalAmount"] = base_amount + gst_amount

                await self.db.create(OrderItem, i_dict)

            return {"success": True, "OrderId": order_id}

        except Exception as e:
            logger.error(f"Create order error: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db.disconnect()


    # ------------------------
    # Get Order by OrderId with full customer, retailer
    # ------------------------
    async def get_order(self, order_id: int):
        try:
            await self.db.connect()

            # Fetch order
            order_list = await self.db.read(Order, {"OrderId": order_id})
            if not order_list:
                return {"success": False, "message": "Order not found"}
            order = order_list[0]

            # Fetch order items
            items = await self.db.read(OrderItem, {"OrderId": order.OrderId})
            item_data = [
                {
                    "MedicineId": i.MedicineId,
                    "MedicineName": getattr(i, "MedicineName", ""),  # optional if model has name
                    "Quantity": i.Quantity,
                    "UnitPrice": getattr(i, "UnitPrice", 0),
                    "GSTPercentage": getattr(i, "GSTPercentage", 0),
                    "TotalAmount": i.TotalAmount
                }
                for i in items
            ]

            # Fetch retailer info
            # retailer_list = await self.db.read(Retailer, {"RetailerId": order.RetailerId})
            # retailer = retailer_list[0] if retailer_list else None
            # retailer_info = {
            #     "RetailerId": retailer.RetailerId if retailer else None,
            #     "ShopName": retailer.ShopName if retailer else "",
            #     "OwnerName": retailer.OwnerName if retailer else "",
            #     "PhoneNumber": retailer.PhoneNumber if retailer else "",
            #     "Email": retailer.Email if retailer else "",
            #     "AddressLine1": retailer.AddressLine1 if retailer else "",
            #     "AddressLine2": retailer.AddressLine2 if retailer else "",
            #     "City": retailer.City if retailer else "",
            #     "State": retailer.State if retailer else "",
            #     "Country": retailer.Country if retailer else "",
            #     "PostalCode": retailer.PostalCode if retailer else ""
            # }

            # Fetch customer info
            customer_list = await self.db.read(Customer, {"CustomerId": order.CustomerId})
            customer = customer_list[0] if customer_list else None


            customer_info = {
                "CustomerId": customer.CustomerId if customer else None,
                "FullName": customer.FullName if customer else "",
                "PhoneNumber": customer.PhoneNumber if customer else "",
                "Email": customer.Email if customer else "",
                "AddressLine1": customer.AddressLine1 if customer else "",
                "AddressLine2": customer.AddressLine2 if customer else "",
                "City": customer.City if customer else "",
                "State": customer.State if customer else "",
                "Country": customer.Country if customer else "",
                "PostalCode": customer.PostalCode if customer else "",
                "Latitude": customer.Latitude if customer else None,
                "Longitude": customer.Longitude if customer else None
            }

            return {
                "success": True,
                "OrderId": order.OrderId,
                "Amount": order.Amount,
                "OrderDate": order.OrderDateTime,
                "Status": order.OrderStatus,
                "OrderStage": order.OrderStage,
                "DeliveryMode": order.DeliveryMode,
                "DeliveryService": order.DeliveryService,
                "DeliveryPartnerTrackingId": order.DeliveryPartnerTrackingId,
                "PaymentMode": order.PaymentMode,
                "PaymentStatus": order.PaymentStatus,
                "InvoiceId": order.InvoiceId,
                "PrescriptionFileUrl": order.PrescriptionFileUrl,
                "PrescriptionVerified": order.PrescriptionVerified,
                "Customer": customer_info,
                # "Retailer": retailer_info,
                "Items": item_data
            }

        except Exception as e:
            logger.error(f"Get order error: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db.disconnect()



    # ------------------------
    # Update Order
    # ------------------------
    async def update_order(self, order_id: int, data: dict):
        try:
            await self.db.connect()
            data["UpdatedAt"] = ist_now()
            updated = await self.db.update(Order, {"OrderId": order_id}, data)
            if updated:
                return {"success": True, "message": "Order updated"}
            return {"success": False, "message": "Order not found"}
        except Exception as e:
            logger.error(f"Update order error: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db.disconnect()

    # ------------------------
    # Delete Order
    # ------------------------
    async def delete_order(self, order_id: int):
        try:
            await self.db.connect()
            await self.db.delete(OrderItem, {"OrderId": order_id})
            deleted = await self.db.delete(Order, {"OrderId": order_id})
            if deleted:
                return {"success": True, "message": "Order deleted"}
            return {"success": False, "message": "Order not found"}
        except Exception as e:
            logger.error(f"Delete order error: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db.disconnect()

    # ------------------------
    # Get all orders by Customer
    # ------------------------
    async def get_orders_by_customer(self, customer_id: int):
        try:
            await self.db.connect()
            orders = await self.db.read(Order, {"CustomerId": customer_id})
            if not orders:
                return {"TotalOrders": 0, "Delivered": 0, "Processing": 0, "Pending": 0, "Orders": []}

            result = {"TotalOrders": len(orders), "Delivered": 0, "Processing": 0, "Pending": 0, "Orders": []}

            for o in orders:
                if o.OrderStatus == "Delivered":
                    result["Delivered"] += 1
                elif o.OrderStatus == "Processing":
                    result["Processing"] += 1
                else:
                    result["Pending"] += 1

                # retailer_list = await self.db.read(Retailer, {"RetailerId": o.RetailerId})
                # retailer = retailer_list[0] if retailer_list else None

                # items = await self.db.read(OrderItem, {"OrderId": o.OrderId})
                # items_count = len(items)

                # result["Orders"].append({
                #     "OrderId": o.OrderId,
                #     "RetailerName": retailer.ShopName if retailer else "",
                #     "RetailerContact": retailer.PhoneNumber if retailer else "",
                #     "ItemsCount": items_count,
                #     "Amount": o.Amount,
                #     "OrderDate": o.OrderDateTime,
                #     "Status": o.OrderStatus
                # })

            return result

        except Exception as e:
            logger.error(f"Get orders by customer error: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db.disconnect()

    # ------------------------
    # Get all orders by Retailer
    # ------------------------
    async def get_orders_by_retailer(self, retailer_id: int):
        try:
            await self.db.connect()
            orders = await self.db.read(Order, {"RetailerId": retailer_id})
            if not orders:
                return {"TotalOrders": 0, "Delivered": 0, "Processing": 0, "Pending": 0, "NewOrders": []}

            result = {"TotalOrders": len(orders), "Delivered": 0, "Processing": 0, "Pending": 0, "NewOrders": []}

            for o in orders:
                if o.OrderStatus == "Delivered":
                    result["Delivered"] += 1
                elif o.OrderStatus == "Processing":
                    result["Processing"] += 1
                else:
                    result["Pending"] += 1

                customer_list = await self.db.read(Customer, {"CustomerId": o.CustomerId})
                customer = customer_list[0] if customer_list else None

                items = await self.db.read(OrderItem, {"OrderId": o.OrderId})
                med_list = [{"MedicineName": i.MedicineName, "Quantity": i.Quantity} for i in items]

                result["NewOrders"].append({
                    "OrderId": o.OrderId,
                    "CustomerName": customer.FullName if customer else "",
                    "OrderDate": o.OrderDateTime,
                    "MedicineRequested": med_list
                })

            return result
        except Exception as e:
            logger.error(f"Get orders by retailer error: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db.disconnect()




class OrderItemManager:
    def __init__(self, db_type: str):
        self.db = DatabaseManager(db_type)

    # -------------------------------------------------------------
    # Create Order Item
    # -------------------------------------------------------------
    async def create_order_item(self, item_data: OrderItemCreate):
        try:
            await self.db.connect()
            item_dict = item_data.dict()
            obj = await self.db.create(OrderItem, item_dict)

            return {
                "success": True,
                "message": "Order item created successfully",
                "data": obj.__dict__
            }
        except Exception as e:
            logger.error(f"Create order item failed: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db.disconnect()

    # -------------------------------------------------------------
    # Get Order Item by ItemId
    # -------------------------------------------------------------
    async def get_order_item(self, item_id: int):
        try:
            await self.db.connect()
            result = await self.db.read(OrderItem, {"ItemId": item_id})

            if not result:
                return {"success": False, "message": "Order item not found"}

            return {"success": True, "data": result[0].__dict__}
        except Exception as e:
            logger.error(f"Get order item failed: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db.disconnect()

    # -------------------------------------------------------------
    # Get all items for an Order
    # -------------------------------------------------------------
    async def get_items_by_order(self, order_id: int):
        try:
            await self.db.connect()
            result = await self.db.read(OrderItem, {"OrderId": order_id})

            return {
                "success": True,
                "data": [item.__dict__ for item in result]
            }
        except Exception as e:
            logger.error(f"Get items by order failed: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db.disconnect()

    # -------------------------------------------------------------
    # Update Order Item
    # -------------------------------------------------------------
    async def update_order_item(self, item_id: int, data: OrderItemUpdate):
        try:
            await self.db.connect()

            update_data = data.dict(exclude_unset=True)
            rowcount = await self.db.update(OrderItem, {"ItemId": item_id}, update_data)

            if rowcount:
                return {"success": True, "message": "Order item updated"}
            return {"success": False, "message": "Order item not found"}

        except Exception as e:
            logger.error(f"Update order item failed: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db.disconnect()

    # -------------------------------------------------------------
    # Delete Order Item
    # -------------------------------------------------------------
    async def delete_order_item(self, item_id: int):
        try:
            await self.db.connect()
            deleted = await self.db.delete(OrderItem, {"ItemId": item_id})

            if deleted:
                return {"success": True, "message": "Order item deleted"}
            return {"success": False, "message": "Order item not found"}
        except Exception as e:
            logger.error(f"Delete order item failed: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db.disconnect()
