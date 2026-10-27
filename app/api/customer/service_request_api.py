from fastapi import APIRouter, HTTPException
from ...config import settings
from ...crud.customer.service_request_manager import ServiceRequestManager
from ...schemas.customer.service_request_schema import (
    ServiceRequestCreate,
    ServiceRequestUpdate
)


class ServiceRequestAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = ServiceRequestManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/requests")(self.create)
        self.router.get("/requests/{id}")(self.get)
        self.router.get("/requests")(self.get_all)
        self.router.put("/requests/{id}")(self.update)
        self.router.delete("/requests/{id}")(self.delete)

        self.router.put("/requests/{id}/status")(self.update_status)
        self.router.get("/requests/provider/{provider_id}")(self.get_by_provider)
        self.router.get("/requests/customer/{customer_id}")(self.get_by_customer)
        self.router.get("/requests/auto-assign")(self.auto_assign)

    async def create(self, payload: ServiceRequestCreate):
        return await self.crud.create(payload)

    async def get(self, id: int):
        return await self.crud.get(id)

    async def get_all(self):
        return await self.crud.get_all()

    async def update(self, id: int, payload: ServiceRequestUpdate):
        return await self.crud.update(id, payload)

    async def delete(self, id: int):
        return await self.crud.delete(id)

    async def update_status(self, id: int, status: str):
        return await self.crud.update_status(id, status)

    async def get_by_provider(self, provider_id: int):
        return await self.crud.get_by_provider(provider_id)

    async def get_by_customer(self, customer_id: int):
        return await self.crud.get_by_customer(customer_id)

    async def auto_assign(self, pincode: str, service_list_id: int):
        return await self.crud.auto_assign(pincode, service_list_id)