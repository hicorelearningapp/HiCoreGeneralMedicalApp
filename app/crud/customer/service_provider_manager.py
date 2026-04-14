from typing import Optional
from ...utils.logger import get_logger
from ...db.base.database_manager import DatabaseManager
from ...models.customer.service_provider_model import ServiceProvider
from ...schemas.customer.service_provider_schema import (
    ServiceProviderCreate,
    ServiceProviderUpdate,
    ServiceProviderRead
)
import hashlib

logger = get_logger(__name__)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class ServiceProviderManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_provider(self, provider: ServiceProviderCreate) -> dict:
        try:
            await self.db_manager.connect()

            data = provider.dict()
            plain_password = data.pop("Password", None)

            if plain_password:
                data["PasswordHash"] = hash_password(plain_password)

            existing = await self.db_manager.read(ServiceProvider, {"Email": data["Email"]})
            if existing:
                return {"success": False, "message": "Email already registered"}

            obj = await self.db_manager.create(ServiceProvider, data)

            return {
                "success": True,
                "message": "Service provider created successfully",
                "data": ServiceProviderRead.from_orm(obj).dict()
            }

        except Exception as e:
            logger.error(f"Error creating provider: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    async def get_provider(self, provider_id: int):
        try:
            await self.db_manager.connect()
            result = await self.db_manager.read(ServiceProvider, {"ServiceProviderId": provider_id})

            if result:
                return {
                    "success": True,
                    "message": "Fetched successfully",
                    "data": ServiceProviderRead.from_orm(result[0]).dict()
                }

            return {"success": False, "message": "Not found", "data": None}

        finally:
            await self.db_manager.disconnect()

    async def get_all_providers(self):
        try:
            await self.db_manager.connect()
            result = await self.db_manager.read(ServiceProvider)

            return {
                "success": True,
                "message": "Fetched successfully",
                "data": [ServiceProviderRead.from_orm(p).dict() for p in result]
            }

        finally:
            await self.db_manager.disconnect()

    async def update_provider(self, provider_id: int, data: ServiceProviderUpdate):
        try:
            await self.db_manager.connect()

            update_data = data.dict(exclude_unset=True)

            if "Password" in update_data:
                password = update_data.pop("Password")
                if password:
                    update_data["PasswordHash"] = hash_password(password)

            rowcount = await self.db_manager.update(
                ServiceProvider,
                {"ServiceProviderId": provider_id},
                update_data
            )

            return {
                "success": bool(rowcount),
                "message": "Updated" if rowcount else "No changes",
                "data": {"rows_affected": rowcount}
            }

        finally:
            await self.db_manager.disconnect()

    async def delete_provider(self, provider_id: int):
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.delete(ServiceProvider, {"ServiceProviderId": provider_id})

            return {
                "success": bool(rowcount),
                "message": "Deleted" if rowcount else "Not found",
                "data": {"rows_affected": rowcount}
            }

        finally:
            await self.db_manager.disconnect()

    async def register(self, email: str, password: str):
        await self.db_manager.connect()

        existing = await self.db_manager.read(ServiceProvider, {"Email": email})
        if existing:
            await self.db_manager.disconnect()
            return {"success": False, "message": "Email already registered"}

        provider = await self.db_manager.create(
            ServiceProvider,
            {
                "Email": email,
                "PasswordHash": hash_password(password),
            },
        )

        await self.db_manager.disconnect()

        return {
            "success": True,
            "message": "Registered successfully",
            "data": {"ServiceProviderId": provider.ServiceProviderId, "Email": provider.Email},
        }

    async def login(self, email: str, password: str):
        await self.db_manager.connect()

        result = await self.db_manager.read(ServiceProvider, {"Email": email})
        if not result:
            return {"success": False, "message": "Invalid credentials"}

        provider = result[0]

        if provider.PasswordHash != hash_password(password):
            return {"success": False, "message": "Invalid credentials"}

        return {
            "success": True,
            "message": "Login successful",
            "data": {"ServiceProviderId": provider.ServiceProviderId, "Email": provider.Email},
        }