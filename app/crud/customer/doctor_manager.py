from ...utils.timezone import ist_now
from ...db.base.database_manager import DatabaseManager
from ...utils.logger import get_logger
from ...models.customer.doctor_model import Doctor, DoctorAppointment
from ...schemas.customer.doctor_schema import (
    DoctorCreate, DoctorUpdate,
    DoctorAppointmentCreate, DoctorAppointmentUpdate
)

logger = get_logger(__name__)


# ------------------------------------------------------
# Doctor Manager
# ------------------------------------------------------
class DoctorManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_doctor(self, data: DoctorCreate):
        try:
            await self.db_manager.connect()
            payload = data.dict()
            payload["CreatedAt"] = ist_now()
            payload["UpdatedAt"] = ist_now()
            obj = await self.db_manager.create(Doctor, payload)
            return {"success": True, "message": "Doctor created", "Doctor Id": obj.DoctorId}
        finally:
            await self.db_manager.disconnect()

    async def get_doctors(self):
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(Doctor, {})
        finally:
            await self.db_manager.disconnect()

    async def get_doctor_by_id(self, doctor_id: int):
        try:
            await self.db_manager.connect()
            rows = await self.db_manager.read(Doctor, {"DoctorId": doctor_id})
            return rows[0] if rows else None
        finally:
            await self.db_manager.disconnect()

    async def update_doctor(self, doctor_id: int, data: DoctorUpdate):
        try:
            await self.db_manager.connect()
            payload = data.dict(exclude_unset=True)
            payload["UpdatedAt"] = ist_now()
            updated = await self.db_manager.update(Doctor, {"DoctorId": doctor_id}, payload)
            return {"success": bool(updated)}
        finally:
            await self.db_manager.disconnect()

    async def delete_doctor(self, doctor_id: int):
        try:
            await self.db_manager.connect()
            deleted = await self.db_manager.delete(Doctor, {"DoctorId": doctor_id})
            return {"success": bool(deleted)}
        finally:
            await self.db_manager.disconnect()


# ------------------------------------------------------
# Appointment Manager
# ------------------------------------------------------
class DoctorAppointmentManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_appointment(self, data: DoctorAppointmentCreate):
        try:
            await self.db_manager.connect()
            payload = data.dict()

            payload["CreatedAt"] = ist_now()
            payload["UpdatedAt"] = ist_now()

            obj = await self.db_manager.create(DoctorAppointment, payload)
            return {"success": True, "message": "Doctor Appointment created", "Doctor Appointment Id": obj.AppointmentId}
        finally:
            await self.db_manager.disconnect()

    async def get_appointment_by_id(self, appointment_id: int):
        try:
            await self.db_manager.connect()
            rows = await self.db_manager.read(DoctorAppointment, {"AppointmentId": appointment_id})
            return rows[0] if rows else None
        finally:
            await self.db_manager.disconnect()

    async def get_appointments_by_doctor(self, doctor_id: int):
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(DoctorAppointment, {"DoctorId": doctor_id})
        finally:
            await self.db_manager.disconnect()

    async def update_appointment(self, appointment_id: int, data: DoctorAppointmentUpdate):
        try:
            await self.db_manager.connect()
            payload = data.dict(exclude_unset=True)
            payload["UpdatedAt"] = ist_now()
            updated = await self.db_manager.update(
                DoctorAppointment, {"AppointmentId": appointment_id}, payload
            )
            return {"success": bool(updated)}
        finally:
            await self.db_manager.disconnect()

    async def delete_appointment(self, appointment_id: int):
        try:
            await self.db_manager.connect()
            deleted = await self.db_manager.delete(
                DoctorAppointment, {"AppointmentId": appointment_id}
            )
            return {"success": bool(deleted)}
        finally:
            await self.db_manager.disconnect()
