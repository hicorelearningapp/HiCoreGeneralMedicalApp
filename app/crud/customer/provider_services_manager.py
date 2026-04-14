from ...utils.logger import get_logger
from ...db.base.database_manager import DatabaseManager
from ...models.customer.provider_services_model import ProviderServices
from ...schemas.customer.provider_services_schema import (
    ProviderServicesCreate,
    ProviderServicesUpdate,
    ProviderServicesRead,
    ProviderServicesBulkCreate
)

logger = get_logger(__name__)


class ProviderServicesManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    # -------------------------------
    # CREATE SINGLE
    # -------------------------------
    async def create(self, payload: ProviderServicesCreate):
        try:
            await self.db_manager.connect()

            obj = await self.db_manager.create(
                ProviderServices,
                payload.dict()
            )

            return {
                "success": True,
                "message": "Service added to provider",
                "data": ProviderServicesRead.from_orm(obj).dict()
            }

        except Exception as e:
            logger.error(e)
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # GET SINGLE
    # -------------------------------
    async def get(self, id: int):
        try:
            await self.db_manager.connect()

            result = await self.db_manager.read(
                ProviderServices,
                {"ProviderServiceId": id}
            )

            if result:
                return {
                    "success": True,
                    "message": "Fetched successfully",
                    "data": ProviderServicesRead.from_orm(result[0]).dict()
                }

            return {"success": False, "message": "Not found", "data": None}

        except Exception as e:
            logger.error(e)
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # GET ALL
    # -------------------------------
    async def get_all(self):
        try:
            await self.db_manager.connect()

            result = await self.db_manager.read(ProviderServices)

            return {
                "success": True,
                "message": "Fetched successfully",
                "data": [ProviderServicesRead.from_orm(r).dict() for r in result]
            }

        except Exception as e:
            logger.error(e)
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # UPDATE
    # -------------------------------
    async def update(self, id: int, payload: ProviderServicesUpdate):
        try:
            await self.db_manager.connect()

            update_data = payload.dict(exclude_unset=True)

            rowcount = await self.db_manager.update(
                ProviderServices,
                {"ProviderServiceId": id},
                update_data
            )

            return {
                "success": bool(rowcount),
                "message": "Updated successfully" if rowcount else "No changes",
                "data": {"rows_affected": rowcount}
            }

        except Exception as e:
            logger.error(e)
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # DELETE
    # -------------------------------
    async def delete(self, id: int):
        try:
            await self.db_manager.connect()

            rowcount = await self.db_manager.delete(
                ProviderServices,
                {"ProviderServiceId": id}
            )

            return {
                "success": bool(rowcount),
                "message": "Deleted" if rowcount else "Not found",
                "data": {"rows_affected": rowcount}
            }

        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # CUSTOM 1: GET BY PROVIDER
    # -------------------------------
    async def get_by_provider(self, provider_id: int):
        try:
            await self.db_manager.connect()

            result = await self.db_manager.read(
                ProviderServices,
                {"ServiceProviderId": provider_id}
            )

            return {
                "success": True,
                "message": "Fetched provider services",
                "data": [ProviderServicesRead.from_orm(r).dict() for r in result]
            }

        except Exception as e:
            logger.error(e)
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # CUSTOM 2: BULK ADD
    # -------------------------------
    async def bulk_add_services(self, payload: ProviderServicesBulkCreate):
        try:
            await self.db_manager.connect()

            created_items = []

            for service in payload.Services:
                data = service.dict()
                data["ServiceProviderId"] = payload.ServiceProviderId

                obj = await self.db_manager.create(ProviderServices, data)
                created_items.append(ProviderServicesRead.from_orm(obj).dict())

            return {
                "success": True,
                "message": "Multiple services added",
                "data": created_items
            }

        except Exception as e:
            logger.error(e)
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()