from fastapi import APIRouter, HTTPException
from ...config import settings
from ...crud.customer.provider_services_manager import ProviderServicesManager
from ...schemas.customer.provider_services_schema import (
    ProviderServicesCreate,
    ProviderServicesUpdate,
    ProviderServicesBulkCreate
)


class ProviderServicesAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = ProviderServicesManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/provider-services", response_model=dict)(self.create)
        self.router.get("/provider-services/{id}", response_model=dict)(self.get)
        self.router.get("/provider-services", response_model=dict)(self.get_all)
        self.router.put("/provider-services/{id}", response_model=dict)(self.update)
        self.router.delete("/provider-services/{id}", response_model=dict)(self.delete)

        # ✅ Custom endpoints
        self.router.get("/provider-services/provider/{provider_id}", response_model=dict)(self.get_by_provider)
        self.router.post("/provider-services/bulk", response_model=dict)(self.bulk_add_services)

    # -------------------------------
    # CREATE
    # -------------------------------
    async def create(self, payload: ProviderServicesCreate):
        try:
            return await self.crud.create(payload)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # GET SINGLE
    # -------------------------------
    async def get(self, id: int):
        try:
            return await self.crud.get(id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # GET ALL
    # -------------------------------
    async def get_all(self):
        try:
            return await self.crud.get_all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # UPDATE
    # -------------------------------
    async def update(self, id: int, payload: ProviderServicesUpdate):
        try:
            return await self.crud.update(id, payload)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # DELETE
    # -------------------------------
    async def delete(self, id: int):
        try:
            return await self.crud.delete(id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # CUSTOM 1
    # -------------------------------
    async def get_by_provider(self, provider_id: int):
        try:
            return await self.crud.get_by_provider(provider_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # CUSTOM 2
    # -------------------------------
    async def bulk_add_services(self, payload: ProviderServicesBulkCreate):
        try:
            return await self.crud.bulk_add_services(payload)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))