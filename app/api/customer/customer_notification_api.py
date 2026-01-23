from fastapi import APIRouter, HTTPException
from typing import Optional
from ...config import settings
from ...crud.customer.customer_notification_manager import CustomerNotificationManager
from ...schemas.customer.customer_notification_schema import CustomerNotificationCreate


class CustomerNotificationAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = CustomerNotificationManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/customers/notifications")(self.create_notification)
        self.router.get("/customers/{customer_id}/notifications")(self.get_notifications)
        self.router.put("/customers/notifications/{notification_id}/read")(self.mark_as_read)
        self.router.delete("/customers/notifications/{notification_id}")(self.delete_notification)
        self.router.delete("/customers/{customer_id}/notifications")(self.delete_all_notifications)

    # ------------------------------------------------------------
    # 🟢 Create Notification
    # ------------------------------------------------------------
    async def create_notification(self, notification: CustomerNotificationCreate):
        try:
            return await self.crud.create_notification(notification)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # ------------------------------------------------------------
    # 🟡 Get Notifications by Customer
    # ------------------------------------------------------------
    async def get_notifications(self, customer_id: int):
        try:
            return await self.crud.get_notifications(customer_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # ------------------------------------------------------------
    # 🟠 Mark Notification as Read
    # ------------------------------------------------------------
    async def mark_as_read(self, notification_id: int):
        try:
            return await self.crud.mark_as_read(notification_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # ------------------------------------------------------------
    # 🔴 Delete Single Notification
    # ------------------------------------------------------------
    async def delete_notification(self, notification_id: int):
        try:
            return await self.crud.delete_notification(notification_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # ------------------------------------------------------------
    # 🗑️ Delete All Notifications for a Customer
    # ------------------------------------------------------------
    async def delete_all_notifications(self, customer_id: int):
        try:
            return await self.crud.delete_all_notifications(customer_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
