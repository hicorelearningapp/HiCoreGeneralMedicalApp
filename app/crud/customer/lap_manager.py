from ...utils.timezone import ist_now
from typing import List, Optional
from ...db.base.database_manager import DatabaseManager
from ...utils.logger import get_logger
from ...models.customer.lap_model import Lab, Test, Appointment
from ...schemas.customer.lap_schema import (
    LabCreate, LabUpdate,
    TestCreate, TestUpdate,
    AppointmentCreate, AppointmentUpdate
)

logger = get_logger(__name__)


# ============================================
# LAB MANAGER
# ============================================
class LabManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_lab(self, data: LabCreate):
        try:
            await self.db_manager.connect()
            payload = data.dict()
            payload["CreatedAt"] = ist_now()
            payload["UpdatedAt"] = ist_now()
            obj = await self.db_manager.create(Lab, payload)
            return {"success": True, "message": "Lab created", "Lab Id": obj.LabId}
        finally:
            await self.db_manager.disconnect()

    async def get_labs(self):
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(Lab, {})
        finally:
            await self.db_manager.disconnect()

    async def get_lab_by_id(self, lab_id: int):
        try:
            await self.db_manager.connect()
            rows = await self.db_manager.read(Lab, {"LabId": lab_id})
            return rows[0] if rows else None
        finally:
            await self.db_manager.disconnect()

    async def get_labs_by_postal(self, postal: str):
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(Lab, {"PostalCode": postal})
        finally:
            await self.db_manager.disconnect()

    async def update_lab(self, lab_id: int, data: LabUpdate):
        try:
            await self.db_manager.connect()
            payload = data.dict(exclude_unset=True)
            payload["UpdatedAt"] = ist_now()
            updated = await self.db_manager.update(Lab, {"LabId": lab_id}, payload)
            return {"success": bool(updated)}
        finally:
            await self.db_manager.disconnect()

    async def delete_lab(self, lab_id: int):
        try:
            await self.db_manager.connect()
            deleted = await self.db_manager.delete(Lab, {"LabId": lab_id})
            return {"success": bool(deleted)}
        finally:
            await self.db_manager.disconnect()


# ============================================
# TEST MANAGER
# ============================================
class TestManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_test(self, data: TestCreate):
        try:
            await self.db_manager.connect()
            payload = data.dict()
            payload["CreatedAt"] = ist_now()
            payload["UpdatedAt"] = ist_now()
            obj = await self.db_manager.create(Test, payload)
            return {"success": True, "message": "Test created", "Test Id": obj.TestId}
        finally:
            await self.db_manager.disconnect()

    async def get_test_by_id(self, test_id: int):
        try:
            await self.db_manager.connect()
            rows = await self.db_manager.read(Test, {"TestId": test_id})
            return rows[0] if rows else None
        finally:
            await self.db_manager.disconnect()

    async def get_tests_by_lab(self, lab_id: int):
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(Test, {"LabId": lab_id})
        finally:
            await self.db_manager.disconnect()

    async def update_test(self, test_id: int, data: TestUpdate):
        try:
            await self.db_manager.connect()
            payload = data.dict(exclude_unset=True)
            payload["UpdatedAt"] = ist_now()
            updated = await self.db_manager.update(Test, {"TestId": test_id}, payload)
            return {"success": bool(updated)}
        finally:
            await self.db_manager.disconnect()

    async def delete_test(self, test_id: int):
        try:
            await self.db_manager.connect()
            deleted = await self.db_manager.delete(Test, {"TestId": test_id})
            return {"success": bool(deleted)}
        finally:
            await self.db_manager.disconnect()


# ============================================
# APPOINTMENT MANAGER
# ============================================
class AppointmentManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_appointment(self, data: AppointmentCreate):
        try:
            await self.db_manager.connect()
            payload = data.dict()
            if not payload.get("AppointmentNo"):
                payload["AppointmentNo"] = f"APPT-{int(ist_now().timestamp())}"

            payload["CreatedAt"] = ist_now()
            payload["UpdatedAt"] = ist_now()
            obj = await self.db_manager.create(Appointment, payload)
            return {"success": True, "message": "Appointment created", "Appointment Id": obj.AppointmentId}
        finally:
            await self.db_manager.disconnect()

    async def get_appointment_by_id(self, appointment_id: int):
        try:
            await self.db_manager.connect()
            rows = await self.db_manager.read(Appointment, {"AppointmentId": appointment_id})
            return rows[0] if rows else None
        finally:
            await self.db_manager.disconnect()

    async def get_appointments_by_lab(self, lab_id: int):
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(Appointment, {"LabId": lab_id})
        finally:
            await self.db_manager.disconnect()

    async def update_appointment(self, appointment_id: int, data: AppointmentUpdate):
        try:
            await self.db_manager.connect()
            payload = data.dict(exclude_unset=True)
            payload["UpdatedAt"] = ist_now()
            updated = await self.db_manager.update(Appointment, {"AppointmentId": appointment_id}, payload)
            return {"success": bool(updated)}
        finally:
            await self.db_manager.disconnect()

    async def delete_appointment(self, appointment_id: int):
        try:
            await self.db_manager.connect()
            deleted = await self.db_manager.delete(Appointment, {"AppointmentId": appointment_id})
            return {"success": bool(deleted)}
        finally:
            await self.db_manager.disconnect()
