from typing import List, Optional
from ...db.base.database_manager import DatabaseManager
from ...utils.logger import get_logger
from ...schemas.customer.medicine_schema import (
    MedicalTypeCreate,
    MedicalTypeUpdate,
    MedicineCategoryCreate,
    MedicineCategoryUpdate,
    MedicineCreate,
    MedicineRead,
    MedicineUpdate,
    MedicineInfoCreate,
    MedicineInfoUpdate
)
from ...models.customer.medicine_model import (
    MedicalType,
    MedicineCategory,
    Medicine,
    MedicineInfo
)

logger = get_logger(__name__)

# ============================================================
# MedicalType Manager
# ============================================================
class MedicalTypeManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_medicine_type(self, data: MedicalTypeCreate) -> dict:
        try:
            await self.db_manager.connect()
            obj = await self.db_manager.create(MedicalType, data.dict())
            return {"success": True, "message": "MedicalType created successfully", "MedicalType Id": obj.MedicalTypeId}
        except Exception as e:
            logger.error(f"Error creating MedicalType: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    async def get_medicine_types(self, filters: Optional[dict] = None) -> List[MedicalType]:
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(MedicalType, filters or {})
        except Exception as e:
            logger.error(f"Error fetching MedicalType: {e}")
            return []
        finally:
            await self.db_manager.disconnect()

    async def update_medicine_type(self, mt_id: int, data: MedicalTypeUpdate) -> dict:
        try:
            await self.db_manager.connect()
            count = await self.db_manager.update(MedicalType, {"MedicalTypeId": mt_id}, data.dict(exclude_unset=True))
            if count:
                return {"success": True, "message": "MedicalType updated successfully"}
            return {"success": False, "message": "MedicalType not found"}
        finally:
            await self.db_manager.disconnect()

    async def delete_medicine_type(self, mt_id: int) -> dict:
        try:
            await self.db_manager.connect()
            count = await self.db_manager.delete(MedicalType, {"MedicalTypeId": mt_id})
            if count:
                return {"success": True, "message": "MedicalType deleted successfully"}
            return {"success": False, "message": "MedicalType not found"}
        finally:
            await self.db_manager.disconnect()


# ============================================================
# MedicineCategory Manager
# ============================================================
class MedicineCategoryManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_medicine_category(self, data: MedicineCategoryCreate) -> dict:
        try:
            await self.db_manager.connect()
            obj = await self.db_manager.create(MedicineCategory, data.dict())
            return {"success": True, "message": "MedicineCategory created successfully", "MedicineCategory Id": obj.MedicineCategoryId}
        finally:
            await self.db_manager.disconnect()

    async def get_medicine_categories(self, filters: Optional[dict] = None) -> List[MedicineCategory]:
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(MedicineCategory, filters or {})
        finally:
            await self.db_manager.disconnect()

    async def update_medicine_category(self, mc_id: int, data: MedicineCategoryUpdate) -> dict:
        try:
            await self.db_manager.connect()
            count = await self.db_manager.update(MedicineCategory, {"MedicineCategoryId": mc_id}, data.dict(exclude_unset=True))
            if count:
                return {"success": True, "message": "MedicineCategory updated successfully"}
            return {"success": False, "message": "MedicineCategory not found"}
        finally:
            await self.db_manager.disconnect()

    async def delete_medicine_category(self, mc_id: int) -> dict:
        try:
            await self.db_manager.connect()
            count = await self.db_manager.delete(MedicineCategory, {"MedicineCategoryId": mc_id})
            if count:
                return {"success": True, "message": "MedicineCategory deleted successfully"}
            return {"success": False, "message": "MedicineCategory not found"}
        finally:
            await self.db_manager.disconnect()

    async def get_categories_by_type(self, medicine_type_id: int):
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(MedicineCategory, {"MedicalTypeId": medicine_type_id})
        finally:
            await self.db_manager.disconnect()


# ------------------------------------------------
# Medicine Manager
# ------------------------------------------------
class MedicineManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_medicine(self, data: MedicineCreate) -> dict:
        try:
            await self.db_manager.connect()
            db_data = data.dict()
            obj = await self.db_manager.create(Medicine, db_data)
            return {"success": True, "message": "Medicine created successfully", "MedicineId": obj.MedicineId}
        finally:
            await self.db_manager.disconnect()

    async def get_medicines(self, filters: Optional[dict] = None) -> List[MedicineRead]:
        try:
            await self.db_manager.connect()
            medicines = await self.db_manager.read(Medicine, filters or {})
            return medicines
        finally:
            await self.db_manager.disconnect()

    async def get_medicines_by_category(self, MedicineCategoryId: int) -> List[MedicineRead]:
        try:
            await self.db_manager.connect()
            medicines = await self.db_manager.read(Medicine, {"MedicineCategoryId": MedicineCategoryId})
            return medicines
        finally:
            await self.db_manager.disconnect()

    async def update_medicine(self, medicine_id: int, data: MedicineUpdate) -> dict:
        try:
            await self.db_manager.connect()
            db_data = data.dict(exclude_unset=True)
            count = await self.db_manager.update(Medicine, {"MedicineId": medicine_id}, db_data)
            if count:
                return {"success": True, "message": "Medicine updated successfully"}
            return {"success": False, "message": "Medicine not found"}
        finally:
            await self.db_manager.disconnect()

    async def delete_medicine(self, medicine_id: int) -> dict:
        try:
            await self.db_manager.connect()
            count = await self.db_manager.delete(Medicine, {"MedicineId": medicine_id})
            if count:
                return {"success": True, "message": "Medicine deleted successfully"}
            return {"success": False, "message": "Medicine not found"}
        finally:
            await self.db_manager.disconnect()


# ============================================================
# MedicineInfo Manager
# ============================================================
class MedicineInfoManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_medicine_info(self, data: MedicineInfoCreate) -> dict:
        try:
            await self.db_manager.connect()
            obj = await self.db_manager.create(MedicineInfo, data.dict())
            return {"success": True, "message": "MedicineInfo created successfully", "MedicineInfo Id": obj.MedicineInfoId}
        finally:
            await self.db_manager.disconnect()

    async def get_medicine_infos(self, filters: Optional[dict] = None) -> List[MedicineInfo]:
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(MedicineInfo, filters or {})
        finally:
            await self.db_manager.disconnect()

    async def get_infos_by_medicine_id(self, medicine_id: int):
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(MedicineInfo, {"MedicineId": medicine_id})
        finally:
            await self.db_manager.disconnect()

    async def update_medicine_info(self, mi_id: int, data: MedicineInfoUpdate) -> dict:
        try:
            await self.db_manager.connect()
            count = await self.db_manager.update(MedicineInfo, {"MedicineInfoId": mi_id}, data.dict(exclude_unset=True))
            if count:
                return {"success": True, "message": "MedicineInfo updated successfully"}
            return {"success": False, "message": "MedicineInfo not found"}
        finally:
            await self.db_manager.disconnect()

    async def delete_medicine_info(self, mi_id: int) -> dict:
        try:
            await self.db_manager.connect()
            count = await self.db_manager.delete(MedicineInfo, {"MedicineInfoId": mi_id})
            if count:
                return {"success": True, "message": "MedicineInfo deleted successfully"}
            return {"success": False, "message": "MedicineInfo not found"}
        finally:
            await self.db_manager.disconnect()
