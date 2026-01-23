from fastapi import APIRouter, HTTPException
from ...config import settings
from ...crud.customer.prescription_manager import PrescriptionManager
from ...schemas.customer.prescription_schema import PrescriptionCreate, PrescriptionUpdate

class PrescriptionAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = PrescriptionManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/prescriptions")(self.create_prescription)
        self.router.get("/prescriptions/customer/{customer_id}")(self.get_prescriptions_by_customer)
        self.router.get("/prescriptions/{prescription_id}")(self.get_prescription_by_id)
        self.router.put("/prescriptions/{prescription_id}")(self.update_prescription)
        self.router.delete("/prescriptions/{prescription_id}")(self.delete_prescription)

    # -----------------------------
    async def create_prescription(self, prescription: PrescriptionCreate):
        return await self.crud.create_prescription(prescription)

    # -----------------------------
    async def get_prescriptions_by_customer(self, customer_id: int):
        return await self.crud.get_prescriptions(customer_id)

    # -----------------------------
    async def get_prescription_by_id(self, prescription_id: int):
        return await self.crud.get_prescription_by_id(prescription_id)

    # -----------------------------
    async def update_prescription(self, prescription_id: int, update: PrescriptionUpdate):
        return await self.crud.update_prescription(prescription_id, update.dict(exclude_unset=True))

    # -----------------------------
    async def delete_prescription(self, prescription_id: int):
        return await self.crud.delete_prescription(prescription_id)
