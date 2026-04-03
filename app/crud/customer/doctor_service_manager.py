from ...db.base.database_manager import DatabaseManager
from ...utils.logger import get_logger
from ...models.customer.doctor_service_model import DoctorService
from ...schemas.customer.doctor_service_schema import (
    DoctorServiceCreate, DoctorServiceUpdate
)

logger = get_logger(__name__)


# ------------------------------------------------------
# Doctor Service Manager
# ------------------------------------------------------
class DoctorServiceManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_doctor_service(self, data: DoctorServiceCreate):
        try:
            await self.db_manager.connect()
            payload = data.dict()
            obj = await self.db_manager.create(DoctorService, payload)
            return {"success": True, "message": "Doctor Service created", "Doctor Service Id": obj.DoctorServiceId}
        finally:
            await self.db_manager.disconnect()

    async def get_doctor_services(self):
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(DoctorService, {})
        finally:
            await self.db_manager.disconnect()

    async def get_doctor_service_by_id(self, service_id: int):
        try:
            await self.db_manager.connect()
            rows = await self.db_manager.read(DoctorService, {"DoctorServiceId": service_id})
            return rows[0] if rows else None
        finally:
            await self.db_manager.disconnect()

    async def update_doctor_service(self, service_id: int, data: DoctorServiceUpdate):
        try:
            await self.db_manager.connect()
            payload = data.dict(exclude_unset=True)
            updated = await self.db_manager.update(DoctorService, {"DoctorServiceId": service_id}, payload)
            return {"success": bool(updated)}
        finally:
            await self.db_manager.disconnect()

    async def delete_doctor_service(self, service_id: int):
        try:
            await self.db_manager.connect()
            deleted = await self.db_manager.delete(DoctorService, {"DoctorServiceId": service_id})
            return {"success": bool(deleted)}
        finally:
            await self.db_manager.disconnect()