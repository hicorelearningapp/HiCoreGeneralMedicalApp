from fastapi import APIRouter, HTTPException
from ...config import settings
from ...crud.customer.service_list_manager import ServiceListManager
from ...schemas.customer.service_list_schema import (
    ServiceListCreate,
    ServiceListUpdate
)


class ServiceListAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = ServiceListManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/services", response_model=dict)(self.create_service)
        self.router.get("/services/{service_id}", response_model=dict)(self.get_service)
        self.router.get("/services", response_model=dict)(self.get_all_services)
        self.router.put("/services/{service_id}", response_model=dict)(self.update_service)
        self.router.delete("/services/{service_id}", response_model=dict)(self.delete_service)

    # -------------------------------
    # CREATE
    # -------------------------------
    async def create_service(self, payload: ServiceListCreate):
        try:
            return await self.crud.create_service(payload)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # GET SINGLE
    # -------------------------------
    async def get_service(self, service_id: int):
        try:
            return await self.crud.get_service(service_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # GET ALL
    # -------------------------------
    async def get_all_services(self):
        try:
            return await self.crud.get_all_services()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # UPDATE
    # -------------------------------
    async def update_service(self, service_id: int, payload: ServiceListUpdate):
        try:
            return await self.crud.update_service(service_id, payload)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # DELETE
    # -------------------------------
    async def delete_service(self, service_id: int):
        try:
            return await self.crud.delete_service(service_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))