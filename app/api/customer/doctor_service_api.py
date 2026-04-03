from fastapi import APIRouter, HTTPException
from ...config import settings
from ...crud.customer.doctor_service_manager import (
    DoctorServiceManager, DoctorServiceCreate, DoctorServiceUpdate
)


# --------------------------------------------------
# Doctor Service API
# --------------------------------------------------
class DoctorServiceAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = DoctorServiceManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/doctor-services")(self.create_doctor_service)
        self.router.get("/doctor-services")(self.get_doctor_services)
        self.router.get("/doctor-services/{service_id}")(self.get_doctor_service_by_id)
        self.router.put("/doctor-services/{service_id}")(self.update_doctor_service)
        self.router.delete("/doctor-services/{service_id}")(self.delete_doctor_service)

    async def create_doctor_service(self, data: DoctorServiceCreate):
        try:
            return await self.manager.create_doctor_service(data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_doctor_services(self):
        return await self.manager.get_doctor_services()

    async def get_doctor_service_by_id(self, service_id: int):
        service = await self.manager.get_doctor_service_by_id(service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Doctor Service not found")
        return service

    async def update_doctor_service(self, service_id: int, data: DoctorServiceUpdate):
        try:
            result = await self.manager.update_doctor_service(service_id, data)
            if not result["success"]:
                raise HTTPException(status_code=404, detail="Doctor Service not found")
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_doctor_service(self, service_id: int):
        try:
            result = await self.manager.delete_doctor_service(service_id)
            if not result["success"]:
                raise HTTPException(status_code=404, detail="Doctor Service not found")
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))