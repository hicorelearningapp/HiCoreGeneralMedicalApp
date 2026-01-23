from fastapi import APIRouter, Query, HTTPException
from ...config import settings
from ...crud.customer.pharmacy_manager import PharmacyManager
from ...schemas.customer.pharmacy_schema import PharmacyCreate, PharmacyUpdate

class PharmacyAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = PharmacyManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        # CRUD
        self.router.post("/pharmacies")(self.create_pharmacy)
        self.router.get("/pharmacies")(self.get_pharmacies)
        self.router.put("/pharmacies/{pharmacy_id}")(self.update_pharmacy)
        self.router.delete("/pharmacies/{pharmacy_id}")(self.delete_pharmacy)

        # Nearby
        self.router.get("/pharmacies/nearby/gps")(self.get_nearby_by_gps)
        self.router.get("/pharmacies/nearby/pincode")(self.get_nearby_by_pincode)

    async def create_pharmacy(self, pharmacy: PharmacyCreate):
        try:
            return await self.manager.create_pharmacy(pharmacy)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_pharmacies(self):
        try:
            return await self.manager.get_pharmacies()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_pharmacy(self, pharmacy_id: int, pharmacy: PharmacyUpdate):
        try:
            return await self.manager.update_pharmacy(pharmacy_id, pharmacy)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_pharmacy(self, pharmacy_id: int):
        try:
            return await self.manager.delete_pharmacy(pharmacy_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_nearby_by_gps(
        self,
        latitude: float = Query(..., description="Current latitude"),
        longitude: float = Query(..., description="Current longitude"),
        radius_km: float = Query(5, description="Search radius in km")
    ):
        try:
            return await self.manager.get_nearby_by_gps(latitude, longitude, radius_km)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_nearby_by_pincode(
        self,
        pincode: str = Query(..., description="Pincode to search nearby pharmacies")
    ):
        try:
            return await self.manager.get_nearby_by_pincode(pincode)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
