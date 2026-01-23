from ...utils.timezone import ist_now
from ...db.base.database_manager import DatabaseManager
from ...models.customer.prescription_model import Prescription
from ...schemas.customer.prescription_schema import PrescriptionCreate, PrescriptionUpdate
from ...utils.logger import get_logger

logger = get_logger(__name__)

class PrescriptionManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    # -------------------------------------------------------------
    # Create prescription
    # -------------------------------------------------------------
    async def create_prescription(self, prescription: PrescriptionCreate):
        try:
            await self.db_manager.connect()
            data = prescription.dict()
            data["UploadedAt"] = ist_now()
            new_record = await self.db_manager.create(Prescription, data)
            logger.info(f"✅ Prescription uploaded for CustomerId {data['CustomerId']}")
            return {
                "success": True,
                "message": "Prescription uploaded successfully",
                "PrescriptionId": new_record.PrescriptionId
            }
        except Exception as e:
            logger.error(f"❌ Error creating prescription: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    # -------------------------------------------------------------
    # Get prescriptions summary by customer
    # -------------------------------------------------------------
    async def get_prescriptions(self, customer_id: int):
        try:
            await self.db_manager.connect()
            prescriptions = await self.db_manager.read(Prescription, {"CustomerId": customer_id})

            total = len(prescriptions)
            delivered = sum(1 for p in prescriptions if p.Status == "Delivered")
            processing = sum(1 for p in prescriptions if p.Status == "Processing")
            pending = sum(1 for p in prescriptions if p.Status == "Pending")
            cancelled = sum(1 for p in prescriptions if p.Status == "Cancelled")

            return {
                "TotalPrescriptions": total,
                "Delivered": delivered,
                "Processing": processing,
                "Pending": pending,
                "Cancelled": cancelled,
                "Prescriptions": prescriptions
            }

        except Exception as e:
            logger.error(f"❌ Error fetching prescriptions: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()


    # -------------------------------------------------------------
    # Get prescription by prescription ID
    # -------------------------------------------------------------
    async def get_prescription_by_id(self, prescription_id: int):
        try:
            await self.db_manager.connect()
            result = await self.db_manager.read(
                Prescription, {"PrescriptionId": prescription_id}
            )
            if not result:
                return {"success": False, "message": "Prescription not found"}

            return result

        except Exception as e:
            logger.error(f"❌ Error fetching prescription: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    # -------------------------------------------------------------
    # Update prescription (PUT)
    # -------------------------------------------------------------
    async def update_prescription(self, prescription_id: int, update: dict):
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.update(
                Prescription,
                {"PrescriptionId": prescription_id},
                update
            )
            if rowcount:
                return {"success": True, "message": "Prescription updated"}

            return {"success": False, "message": "Prescription not found"}

        except Exception as e:
            logger.error(f"❌ Error updating prescription: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    # -------------------------------------------------------------
    # Delete prescription
    # -------------------------------------------------------------
    async def delete_prescription(self, prescription_id: int):
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.delete(Prescription, {"PrescriptionId": prescription_id})
            if rowcount:
                logger.info(f"🗑️ Prescription {prescription_id} deleted")
                return {"success": True, "message": "Prescription deleted"}
            return {"success": False, "message": "Prescription not found"}
        except Exception as e:
            logger.error(f"❌ Error deleting prescription: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()
