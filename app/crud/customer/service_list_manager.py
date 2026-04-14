from ...utils.logger import get_logger
from ...db.base.database_manager import DatabaseManager
from ...models.customer.service_list_model import ServiceList
from ...schemas.customer.service_list_schema import (
    ServiceListCreate,
    ServiceListUpdate,
    ServiceListRead
)

logger = get_logger(__name__)


class ServiceListManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_service(self, service: ServiceListCreate) -> dict:
        try:
            await self.db_manager.connect()

            data = service.dict()

            obj = await self.db_manager.create(ServiceList, data)

            return {
                "success": True,
                "message": "Service created successfully",
                "data": ServiceListRead.from_orm(obj).dict()
            }

        except Exception as e:
            logger.error(f"Error creating service: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    async def get_service(self, service_id: int) -> dict:
        try:
            await self.db_manager.connect()

            result = await self.db_manager.read(ServiceList, {"ServiceListId": service_id})

            if result:
                return {
                    "success": True,
                    "message": "Fetched successfully",
                    "data": ServiceListRead.from_orm(result[0]).dict()
                }

            return {"success": False, "message": "Service not found", "data": None}

        except Exception as e:
            logger.error(f"Error fetching service: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    async def get_all_services(self) -> dict:
        try:
            await self.db_manager.connect()

            result = await self.db_manager.read(ServiceList)

            return {
                "success": True,
                "message": "Fetched successfully",
                "data": [ServiceListRead.from_orm(s).dict() for s in result]
            }

        except Exception as e:
            logger.error(f"Error fetching services: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    async def update_service(self, service_id: int, data: ServiceListUpdate) -> dict:
        try:
            await self.db_manager.connect()

            update_data = data.dict(exclude_unset=True)

            rowcount = await self.db_manager.update(
                ServiceList,
                {"ServiceListId": service_id},
                update_data
            )

            return {
                "success": bool(rowcount),
                "message": "Updated successfully" if rowcount else "No changes",
                "data": {"rows_affected": rowcount}
            }

        except Exception as e:
            logger.error(f"Error updating service: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    async def delete_service(self, service_id: int) -> dict:
        try:
            await self.db_manager.connect()

            rowcount = await self.db_manager.delete(
                ServiceList,
                {"ServiceListId": service_id}
            )

            return {
                "success": bool(rowcount),
                "message": "Deleted successfully" if rowcount else "Not found",
                "data": {"rows_affected": rowcount}
            }

        except Exception as e:
            logger.error(f"Error deleting service: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()