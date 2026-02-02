from fastapi import APIRouter, HTTPException
from ...crud.customer.customer_dashboard_manager import CustomerDashboardManager
from ...config import settings

class CustomerDashboardAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = CustomerDashboardManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.get("/customer/{customer_id}/dashboard")(self.get_dashboard)

    async def get_dashboard(self, customer_id: int):
        try:
            return await self.manager.get_dashboard(customer_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
