from typing import Literal, Optional
from fastapi import APIRouter, HTTPException, Query, Form
from ...config import settings
from ...crud.customer.service_request_manager import ServiceRequestManager
from ...crud.customer.service_provider_manager import ServiceProviderManager


# --------------------------------------------------
# Service Provider Dashboard API (My Services)
# --------------------------------------------------
class ServiceProviderDashboardAPI:
    def __init__(self):
        self.router = APIRouter()
        self.request_manager = ServiceRequestManager(settings.db_type)
        self.provider_manager = ServiceProviderManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        # My Services endpoints
        self.router.get("/provider/{provider_id}/my-services")(self.get_my_services)
        self.router.get("/provider/{provider_id}/my-services/{request_id}")(self.get_service_detail)

        # Provider action endpoints
        self.router.put("/provider/{provider_id}/my-services/{request_id}/accept")(self.accept_service)
        self.router.put("/provider/{provider_id}/my-services/{request_id}/reject")(self.reject_service)
        self.router.put("/provider/{provider_id}/my-services/{request_id}/start")(self.start_service)
        self.router.put("/provider/{provider_id}/my-services/{request_id}/complete")(self.complete_service)
        self.router.put("/provider/{provider_id}/my-services/{request_id}/notes")(self.update_provider_notes)

        # Availability status endpoint
        self.router.put("/provider/{provider_id}/availability")(self.update_availability_status)

    async def get_my_services(
        self,
        provider_id: int,
        status: Optional[Literal["assigned", "accepted", "in_progress", "completed"]] = Query(None)
    ):
        """
        Get all service requests assigned to this provider.
        Filter by status if provided.
        """
        try:
            # Verify provider exists
            provider = await self.provider_manager.get_service_provider_by_id(provider_id)
            if not provider:
                raise HTTPException(status_code=404, detail="Service Provider not found")

            # Get assigned requests
            requests = await self.request_manager.get_service_requests_by_provider(provider_id, status)

            # Format response
            formatted_requests = []
            for req in requests:
                formatted_requests.append({
                    "request_id": req.RequestId,
                    "service_id": req.ServiceId,
                    "service_name": req.ServiceName,
                    "customer_name": req.CustomerName,
                    "customer_phone": req.CustomerPhone,
                    "customer_address": req.CustomerAddress,
                    "appointment_date": req.PreferredDate,
                    "appointment_time": req.PreferredTime,
                    "status": req.Status,
                    "request_description": req.RequestDescription,
                    "pincode": req.Pincode,
                    "estimated_price": req.EstimatedPrice,
                    "final_price": req.FinalPrice,
                    "payment_status": req.PaymentStatus,
                    "assigned_at": req.AssignedAt,
                    "accepted_at": req.AcceptedAt,
                    "completed_at": req.CompletedAt,
                    "provider_notes": req.ProviderNotes,
                    "customer_notes": req.CustomerNotes,
                    "created_at": req.CreatedAt
                })

            return {
                "success": True,
                "count": len(formatted_requests),
                "data": formatted_requests
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_service_detail(self, provider_id: int, request_id: int):
        """
        Get detailed information about a specific service request.
        """
        try:
            # Verify provider exists
            provider = await self.provider_manager.get_service_provider_by_id(provider_id)
            if not provider:
                raise HTTPException(status_code=404, detail="Service Provider not found")

            # Get request
            request = await self.request_manager.get_service_request_by_id(request_id)
            if not request:
                raise HTTPException(status_code=404, detail="Service request not found")

            # Verify request is assigned to this provider
            if request.ServiceProviderId != provider_id:
                raise HTTPException(status_code=403, detail="Request not assigned to this provider")

            # Format detailed response
            return {
                "success": True,
                "data": {
                    "request_id": request.RequestId,
                    "service_id": request.ServiceId,
                    "service_name": request.ServiceName,
                    "customer_id": request.CustomerId,
                    "customer_name": request.CustomerName,
                    "customer_phone": request.CustomerPhone,
                    "customer_address": request.CustomerAddress,
                    "appointment_date": request.PreferredDate,
                    "appointment_time": request.PreferredTime,
                    "status": request.Status,
                    "request_description": request.RequestDescription,
                    "pincode": request.Pincode,
                    "estimated_price": request.EstimatedPrice,
                    "final_price": request.FinalPrice,
                    "payment_status": request.PaymentStatus,
                    "assigned_at": request.AssignedAt,
                    "accepted_at": request.AcceptedAt,
                    "completed_at": request.CompletedAt,
                    "cancelled_at": request.CancelledAt,
                    "provider_notes": request.ProviderNotes,
                    "customer_notes": request.CustomerNotes,
                    "created_at": request.CreatedAt,
                    "updated_at": request.UpdatedAt
                }
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def accept_service(self, provider_id: int, request_id: int):
        """
        Accept an assigned service request.
        """
        try:
            result = await self.request_manager.accept_service_request(request_id, provider_id)

            if not result.get("success"):
                raise HTTPException(status_code=400, detail=result.get("message"))

            return result

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def reject_service(
        self,
        provider_id: int,
        request_id: int,
        ProviderNotes: str = Form(None)
    ):
        """
        Reject an assigned service request.
        """
        try:
            result = await self.request_manager.reject_service_request(
                request_id,
                provider_id,
                provider_notes=ProviderNotes
            )

            if not result.get("success"):
                raise HTTPException(status_code=400, detail=result.get("message"))

            return result

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def start_service(self, provider_id: int, request_id: int):
        """
        Start the service (change status to in_progress).
        """
        try:
            result = await self.request_manager.start_service(request_id, provider_id)

            if not result.get("success"):
                raise HTTPException(status_code=400, detail=result.get("message"))

            return result

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def complete_service(
        self,
        provider_id: int,
        request_id: int,
        FinalPrice: float = Form(None)
    ):
        """
        Complete the service.
        """
        try:
            result = await self.request_manager.complete_service(
                request_id,
                provider_id,
                final_price=FinalPrice
            )

            if not result.get("success"):
                raise HTTPException(status_code=400, detail=result.get("message"))

            return result

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_provider_notes(
        self,
        provider_id: int,
        request_id: int,
        ProviderNotes: str = Form(...)
    ):
        """
        Update provider notes for a service request.
        """
        try:
            result = await self.request_manager.update_provider_notes(
                request_id,
                provider_id,
                provider_notes=ProviderNotes
            )

            if not result.get("success"):
                raise HTTPException(status_code=400, detail=result.get("message"))

            return result

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_availability_status(
        self,
        provider_id: int,
        AvailabilityStatus: Literal["available", "unavailable", "busy"] = Form(...)
    ):
        """
        Update the availability status of the service provider.
        """
        try:
            # Verify provider exists
            provider = await self.provider_manager.get_service_provider_by_id(provider_id)
            if not provider:
                raise HTTPException(status_code=404, detail="Service Provider not found")

            result = await self.provider_manager.update_availability_status(
                provider_id,
                AvailabilityStatus
            )

            if not result.get("success"):
                raise HTTPException(status_code=400, detail=result.get("message"))

            return result

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
