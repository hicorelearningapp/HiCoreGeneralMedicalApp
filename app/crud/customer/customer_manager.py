from typing import List, Optional
from ...utils.logger import get_logger
from ...db.base.database_manager import DatabaseManager
from ...models.customer.customer_model import Customer
from ...schemas.customer.customer_schema import (
    CustomerCreate,
    CustomerUpdate,
    CustomerRead
)

logger = get_logger(__name__)


class CustomerManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_customer(self, customer: CustomerCreate) -> dict:
        try:
            await self.db_manager.connect()

            # Convert CustomerCreate -> dict and handle password hashing externally
            data = customer.dict()
            plain_password = data.pop("Password", None)

            # Your password hashing function should go here
            data["PasswordHash"] = plain_password  # Replace later

            obj = await self.db_manager.create(Customer, data)
            logger.info(f"Created customer {obj.CustomerId}")

            return {
                "success": True,
                "message": "Customer created successfully",
                "data": CustomerRead.from_orm(obj).dict()
            }
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            return {"success": False, "message": f"Error creating customer: {e}"}
        finally:
            await self.db_manager.disconnect()

    async def get_customer(self, customer_id: int) -> dict:
        try:
            await self.db_manager.connect()
            result = await self.db_manager.read(Customer, {"CustomerId": customer_id})

            if result:
                return {
                    "success": True,
                    "message": "Customer fetched successfully",
                    "data": CustomerRead.from_orm(result[0]).dict()
                }
            return {"success": False, "message": "Customer not found", "data": None}

        except Exception as e:
            logger.error(f"Error fetching customer {customer_id}: {e}")
            return {"success": False, "message": f"Error fetching customer: {e}"}
        finally:
            await self.db_manager.disconnect()

    async def get_all_customers(self) -> dict:
        try:
            await self.db_manager.connect()
            result = await self.db_manager.read(Customer)
            customers = [CustomerRead.from_orm(c).dict() for c in result]

            return {
                "success": True,
                "message": "Customers fetched successfully",
                "data": customers
            }

        except Exception as e:
            logger.error(f"Error fetching customers: {e}")
            return {"success": False, "message": f"Error fetching customers: {e}"}
        finally:
            await self.db_manager.disconnect()

    async def update_customer(self, customer_id: int, data: CustomerUpdate) -> dict:
        try:
            await self.db_manager.connect()

            update_data = data.dict(exclude_unset=True)

            # If Password is present -> rename to PasswordHash
            if "Password" in update_data:
                update_data["PasswordHash"] = update_data.pop("Password")

            rowcount = await self.db_manager.update(
                Customer,
                {"CustomerId": customer_id},
                update_data
            )

            if rowcount:
                logger.info(f"Updated customer {customer_id}")
                return {
                    "success": True,
                    "message": "Customer updated successfully",
                    "data": {"rows_affected": rowcount}
                }

            return {
                "success": False,
                "message": "Customer not found or no changes made",
                "data": {"rows_affected": rowcount}
            }

        except Exception as e:
            logger.error(f"Error updating customer {customer_id}: {e}")
            return {"success": False, "message": f"Error updating customer: {e}"}
        finally:
            await self.db_manager.disconnect()

    async def delete_customer(self, customer_id: int) -> dict:
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.delete(Customer, {"CustomerId": customer_id})

            if rowcount:
                logger.info(f"Deleted customer {customer_id}")
                return {
                    "success": True,
                    "message": "Customer deleted successfully",
                    "data": {"rows_affected": rowcount}
                }

            return {
                "success": False,
                "message": "Customer not found",
                "data": {"rows_affected": rowcount}
            }

        except Exception as e:
            logger.error(f"Error deleting customer {customer_id}: {e}")
            return {"success": False, "message": f"Error deleting customer: {e}"}
        finally:
            await self.db_manager.disconnect()



