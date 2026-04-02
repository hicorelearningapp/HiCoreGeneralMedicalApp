from typing import Literal
from ...utils.timezone import ist_now
from ...db.base.database_manager import DatabaseManager
from ...utils.logger import get_logger
from ...models.customer.service_provider_model import ServiceProvider
from ...schemas.customer.service_provider_schema import (
    ServiceProviderCreate, ServiceProviderUpdate
)

logger = get_logger(__name__)


# ------------------------------------------------------
# Service Provider Manager
# ------------------------------------------------------
class ServiceProviderManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_service_provider(self, data: ServiceProviderCreate):
        try:
            await self.db_manager.connect()
            payload = data.dict()
            payload["CreatedAt"] = ist_now()
            payload["UpdatedAt"] = ist_now()
            obj = await self.db_manager.create(ServiceProvider, payload)
            return {"success": True, "message": "Service Provider created", "ServiceProviderId": obj.ServiceProviderId}
        finally:
            await self.db_manager.disconnect()

    async def get_service_providers(
        self,
        service_name: str = None,
        pincode: str = None,
        availability_status: Literal["available", "unavailable", "busy"] = None,
        is_verified: bool = None,
        specialization: str = None
    ):
        try:
            await self.db_manager.connect()
            filters = {}

            if service_name:
                filters["ServiceName"] = service_name

            if pincode:
                filters["Pincode"] = pincode

            if availability_status:
                filters["AvailabilityStatus"] = availability_status

            if is_verified is not None:
                filters["IsVerified"] = is_verified

            if specialization:
                filters["Specialization"] = specialization

            return await self.db_manager.read(ServiceProvider, filters)
        finally:
            await self.db_manager.disconnect()

    async def get_service_provider_by_id(self, service_provider_id: int):
        try:
            await self.db_manager.connect()
            rows = await self.db_manager.read(ServiceProvider, {"ServiceProviderId": service_provider_id})
            return rows[0] if rows else None
        finally:
            await self.db_manager.disconnect()

    async def get_service_provider_by_service_id(self, service_id: str):
        try:
            await self.db_manager.connect()
            rows = await self.db_manager.read(ServiceProvider, {"ServiceId": service_id})
            return rows[0] if rows else None
        finally:
            await self.db_manager.disconnect()

    async def update_service_provider(self, service_provider_id: int, data: ServiceProviderUpdate):
        try:
            await self.db_manager.connect()
            payload = data.dict(exclude_unset=True)
            payload["UpdatedAt"] = ist_now()
            updated = await self.db_manager.update(ServiceProvider, {"ServiceProviderId": service_provider_id}, payload)
            return {"success": bool(updated)}
        finally:
            await self.db_manager.disconnect()

    async def delete_service_provider(self, service_provider_id: int):
        try:
            await self.db_manager.connect()
            deleted = await self.db_manager.delete(ServiceProvider, {"ServiceProviderId": service_provider_id})
            return {"success": bool(deleted)}
        finally:
            await self.db_manager.disconnect()

    async def update_availability_status(
        self,
        service_provider_id: int,
        availability_status: Literal["available", "unavailable", "busy"]
    ):
        """
        Update the availability status of a service provider.
        """
        try:
            await self.db_manager.connect()

            payload = {
                "AvailabilityStatus": availability_status,
                "UpdatedAt": ist_now()
            }

            updated = await self.db_manager.update(
                ServiceProvider,
                {"ServiceProviderId": service_provider_id},
                payload
            )

            return {
                "success": bool(updated),
                "message": f"Availability status updated to {availability_status}" if updated else "Service Provider not found"
            }
        finally:
            await self.db_manager.disconnect()
