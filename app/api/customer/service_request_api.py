from typing import Literal, Optional
from datetime import date
from fastapi import APIRouter, HTTPException, Query, Form
from ...config import settings
from ...crud.customer.service_request_manager import ServiceRequestManager
from ...schemas.customer.service_request_schema import (
    ServiceRequestCreate, ServiceRequestUpdate, AssignProviderRequest
)


# --------------------------------------------------
# Service Request API
# --------------------------------------------------
class ServiceRequestAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = ServiceRequestManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/service-requests")(self.create_service_request)
        self.router.get("/service-requests/customer/{customer_id}")(self.get_requests_by_customer)
        self.router.get("/service-requests/{request_id}")(self.get_request_by_id)
        self.router.put("/service-requests/{request_id}/cancel")(self.cancel_request)
        self.router.put("/service-requests/{request_id}/status")(self.update_request_status)
        self.router.put("/service-requests/{request_id}/assign")(self.assign_service_provider)
        self.router.post("/service-requests/auto-assign")(self.create_and_auto_assign)
        self.router.get("/service-requests/available-providers/list")(self.get_available_providers)

    async def create_service_request(
        self,
        CustomerId: int = Form(...),
        ServiceProviderId: Optional[int] = Form(None),
        ServiceName: str = Form(None),
        CustomerName: str = Form(...),
        CustomerPhone: str = Form(...),
        CustomerAddress: str = Form(...),
        Pincode: str = Form(...),
        PreferredDate: date = Form(None),
        PreferredTime: str = Form(None),
        RequestDescription: str = Form(None),
        EstimatedPrice: float = Form(None),
        AssignmentMode: Literal["random", "visible_profile"] = Form("random"),
        NotificationPreference: Literal["whatsapp", "sms", "both"] = Form("both")
    ):
        """
        Create a new service request.
        If AssignmentMode is "random", auto-assign an available provider.
        If "visible_profile", keep as pending for manual selection.
        """
        try:
            # Create the request
            obj = ServiceRequestCreate(
                CustomerId=CustomerId,
                ServiceProviderId=ServiceProviderId,
                ServiceName=ServiceName,
                CustomerName=CustomerName,
                CustomerPhone=CustomerPhone,
                CustomerAddress=CustomerAddress,
                Pincode=Pincode,
                PreferredDate=PreferredDate,
                PreferredTime=PreferredTime,
                RequestDescription=RequestDescription,
                Status="pending",
                EstimatedPrice=EstimatedPrice,
                AssignmentMode=AssignmentMode,
                NotificationPreference=NotificationPreference
            )

            result = await self.manager.create_service_request(obj)

            if not result.get("success"):
                raise HTTPException(status_code=500, detail="Failed to create service request")

            request_id = result.get("RequestId")

            # If random assignment mode, try to auto-assign
            if AssignmentMode == "random":
                auto_assign_result = await self.manager.auto_assign_provider(
                    request_id=request_id,
                    pincode=Pincode,
                    service_name=ServiceName
                )

                return {
                    "success": True,
                    "message": "Service request created",
                    "RequestId": request_id,
                    "Assignment": auto_assign_result
                }

            return {
                "success": True,
                "message": "Service request created (pending manual assignment)",
                "RequestId": request_id,
                "Status": "pending"
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_requests_by_customer(self, customer_id: int):
        """Get all service requests for a customer."""
        try:
            requests = await self.manager.get_service_requests_by_customer(customer_id)
            return {"success": True, "data": requests}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_request_by_id(self, request_id: int):
        """Get details of a specific service request."""
        try:
            request = await self.manager.get_service_request_by_id(request_id)
            if not request:
                raise HTTPException(status_code=404, detail="Service request not found")
            return {"success": True, "data": request}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def cancel_request(self, request_id: int):
        """Cancel a service request."""
        try:
            # First check if request exists
            request = await self.manager.get_service_request_by_id(request_id)
            if not request:
                raise HTTPException(status_code=404, detail="Service request not found")

            # Check if request can be cancelled
            if request.Status in ["completed", "cancelled"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot cancel request with status: {request.Status}"
                )

            result = await self.manager.cancel_service_request(request_id)
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_request_status(
        self,
        request_id: int,
        Status: Literal["pending", "assigned", "accepted", "in_progress", "completed", "cancelled", "rejected"] = Form(...)
    ):
        """Update the status of a service request."""
        try:
            request = await self.manager.get_service_request_by_id(request_id)
            if not request:
                raise HTTPException(status_code=404, detail="Service request not found")

            result = await self.manager.update_request_status(request_id, Status)
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def assign_service_provider(
        self,
        request_id: int,
        ServiceProviderId: int = Form(...),
        AssignmentMode: Literal["random", "visible_profile"] = Form("visible_profile")
    ):
        """
        Manually assign a service provider to a request.
        Used in visible profile booking model where customer selects a provider.
        """
        try:
            request = await self.manager.get_service_request_by_id(request_id)
            if not request:
                raise HTTPException(status_code=404, detail="Service request not found")

            # Check if request can be assigned
            if request.Status not in ["pending", "assigned"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot assign provider to request with status: {request.Status}"
                )

            result = await self.manager.assign_service_provider(
                request_id=request_id,
                service_provider_id=ServiceProviderId,
                assignment_mode=AssignmentMode
            )

            if not result.get("success"):
                raise HTTPException(status_code=400, detail=result.get("message"))

            return result

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_and_auto_assign(
        self,
        CustomerId: int = Form(...),
        ServiceName: str = Form(None),
        CustomerName: str = Form(...),
        CustomerPhone: str = Form(...),
        CustomerAddress: str = Form(...),
        Pincode: str = Form(...),
        PreferredDate: date = Form(None),
        PreferredTime: str = Form(None),
        RequestDescription: str = Form(None)
    ):
        """
        Create a service request and auto-assign an available provider.
        Simplified endpoint for random assignment model.
        """
        try:
            # Create the request
            obj = ServiceRequestCreate(
                CustomerId=CustomerId,
                ServiceProviderId=None,
                ServiceName=ServiceName,
                CustomerName=CustomerName,
                CustomerPhone=CustomerPhone,
                CustomerAddress=CustomerAddress,
                Pincode=Pincode,
                PreferredDate=PreferredDate,
                PreferredTime=PreferredTime,
                RequestDescription=RequestDescription,
                Status="pending",
                AssignmentMode="random",
                NotificationPreference="both"
            )

            result = await self.manager.create_service_request(obj)

            if not result.get("success"):
                raise HTTPException(status_code=500, detail="Failed to create service request")

            request_id = result.get("RequestId")

            # Auto-assign provider
            auto_assign_result = await self.manager.auto_assign_provider(
                request_id=request_id,
                pincode=Pincode,
                service_name=ServiceName
            )

            return {
                "success": True,
                "message": "Service request created and processed",
                "RequestId": request_id,
                "Assignment": auto_assign_result
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_available_providers(
        self,
        pincode: str = Query(None),
        service_name: str = Query(None)
    ):
        """
        Get list of available providers for visible profile booking.
        Customers can view profiles and choose a provider.
        """
        try:
            providers = await self.manager.get_available_providers(
                pincode=pincode,
                service_name=service_name
            )

            return {
                "success": True,
                "count": len(providers),
                "data": providers
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
