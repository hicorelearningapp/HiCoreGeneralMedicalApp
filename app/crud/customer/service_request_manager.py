from typing import Literal
from ...utils.timezone import ist_now
from ...db.base.database_manager import DatabaseManager
from ...utils.logger import get_logger
from ...models.customer.service_request_model import ServiceRequest
from ...models.customer.service_provider_model import ServiceProvider
from ...schemas.customer.service_request_schema import ServiceRequestCreate, ServiceRequestUpdate
from ...utils.notification_service import service_request_notifications
import random

logger = get_logger(__name__)


# ------------------------------------------------------
# Service Request Manager
# ------------------------------------------------------
class ServiceRequestManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_service_request(self, data: ServiceRequestCreate):
        try:
            await self.db_manager.connect()
            payload = data.dict()
            payload["CreatedAt"] = ist_now()
            payload["UpdatedAt"] = ist_now()
            obj = await self.db_manager.create(ServiceRequest, payload)

            # Trigger notification for request created
            try:
                await service_request_notifications.notify_request_created(
                    phone_number=data.CustomerPhone,
                    request_id=obj.RequestId,
                    service_name=data.ServiceName or "Service Request",
                    preference=data.NotificationPreference
                )
                logger.info(f"Notification triggered for request #{obj.RequestId} created")
            except Exception as notify_err:
                logger.warning(f"Failed to send notification for request #{obj.RequestId}: {notify_err}")

            return {"success": True, "message": "Service Request created", "RequestId": obj.RequestId}
        finally:
            await self.db_manager.disconnect()

    async def get_service_requests_by_customer(self, customer_id: int):
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(ServiceRequest, {"CustomerId": customer_id})
        finally:
            await self.db_manager.disconnect()

    async def get_service_request_by_id(self, request_id: int):
        try:
            await self.db_manager.connect()
            rows = await self.db_manager.read(ServiceRequest, {"RequestId": request_id})
            return rows[0] if rows else None
        finally:
            await self.db_manager.disconnect()

    async def update_service_request(self, request_id: int, data: ServiceRequestUpdate):
        try:
            await self.db_manager.connect()
            payload = data.dict(exclude_unset=True)
            payload["UpdatedAt"] = ist_now()
            updated = await self.db_manager.update(ServiceRequest, {"RequestId": request_id}, payload)
            return {"success": bool(updated)}
        finally:
            await self.db_manager.disconnect()

    async def cancel_service_request(self, request_id: int):
        try:
            await self.db_manager.connect()
            payload = {
                "Status": "cancelled",
                "CancelledAt": ist_now(),
                "UpdatedAt": ist_now()
            }
            updated = await self.db_manager.update(ServiceRequest, {"RequestId": request_id}, payload)

            # Trigger notification for cancelled request
            if updated:
                try:
                    request = await self.get_service_request_by_id(request_id)
                    if request:
                        await service_request_notifications.notify_request_cancelled(
                            phone_number=request.CustomerPhone,
                            request_id=request_id,
                            preference=request.NotificationPreference
                        )
                        logger.info(f"Notification triggered for request #{request_id} cancelled")
                except Exception as notify_err:
                    logger.warning(f"Failed to send cancellation notification: {notify_err}")

            return {"success": bool(updated), "message": "Request cancelled" if updated else "Request not found"}
        finally:
            await self.db_manager.disconnect()

    async def assign_service_provider(
        self,
        request_id: int,
        service_provider_id: int,
        assignment_mode: Literal["random", "visible_profile"] = "random"
    ):
        try:
            await self.db_manager.connect()

            # Verify the service provider exists and is eligible
            provider_rows = await self.db_manager.read(
                ServiceProvider,
                {"ServiceProviderId": service_provider_id}
            )

            if not provider_rows:
                return {"success": False, "message": "Service Provider not found"}

            provider = provider_rows[0]

            # Check eligibility criteria
            if not provider.IsActive:
                return {"success": False, "message": "Service Provider is not active"}

            if provider.AvailabilityStatus != "available":
                return {"success": False, "message": "Service Provider is not available"}

            if not provider.IsVerified:
                return {"success": False, "message": "Service Provider is not verified"}

            # Update the request with assignment
            payload = {
                "ServiceProviderId": service_provider_id,
                "Status": "assigned",
                "AssignedAt": ist_now(),
                "AssignmentMode": assignment_mode,
                "UpdatedAt": ist_now()
            }

            updated = await self.db_manager.update(ServiceRequest, {"RequestId": request_id}, payload)

            if updated:
                # Trigger notification for provider assigned
                try:
                    request = await self.get_service_request_by_id(request_id)
                    if request:
                        await service_request_notifications.notify_provider_assigned(
                            phone_number=request.CustomerPhone,
                            request_id=request_id,
                            provider_name=provider.ProviderName,
                            service_name=request.ServiceName or "Service",
                            preference=request.NotificationPreference
                        )
                        logger.info(f"Notification triggered for provider assigned to request #{request_id}")
                except Exception as notify_err:
                    logger.warning(f"Failed to send assignment notification: {notify_err}")

                return {
                    "success": True,
                    "message": "Service Provider assigned successfully",
                    "ServiceProviderId": service_provider_id,
                    "AssignmentMode": assignment_mode
                }
            else:
                return {"success": False, "message": "Failed to assign Service Provider"}

        finally:
            await self.db_manager.disconnect()

    async def auto_assign_provider(self, request_id: int, work_location: str = None, pincode: str = None):
        """
        Auto-assign an available provider using random assignment model.
        Returns the assigned provider or None if no provider is available.
        """
        try:
            await self.db_manager.connect()

            # Build filters for eligible providers
            filters = {
                "IsActive": True,
                "AvailabilityStatus": "available",
                "IsVerified": True
            }

            if work_location:
                filters["WorkLocation"] = work_location

            if pincode:
                filters["Pincode"] = pincode

            # Get eligible providers
            eligible_providers = await self.db_manager.read(ServiceProvider, filters)

            if not eligible_providers:
                return {
                    "success": False,
                    "message": "No eligible service providers available",
                    "RequestStatus": "pending"
                }

            # Random assignment
            selected_provider = random.choice(eligible_providers)

            # Update the request
            payload = {
                "ServiceProviderId": selected_provider.ServiceProviderId,
                "Status": "assigned",
                "AssignedAt": ist_now(),
                "AssignmentMode": "random",
                "UpdatedAt": ist_now()
            }

            updated = await self.db_manager.update(ServiceRequest, {"RequestId": request_id}, payload)

            if updated:
                # Trigger notification for provider assigned (auto-assign)
                try:
                    request = await self.get_service_request_by_id(request_id)
                    if request:
                        await service_request_notifications.notify_provider_assigned(
                            phone_number=request.CustomerPhone,
                            request_id=request_id,
                            provider_name=selected_provider.ProviderName,
                            service_name=request.ServiceName or "Service",
                            preference=request.NotificationPreference
                        )
                        logger.info(f"Notification triggered for auto-assigned provider on request #{request_id}")
                except Exception as notify_err:
                    logger.warning(f"Failed to send auto-assignment notification: {notify_err}")

                return {
                    "success": True,
                    "message": "Service Provider auto-assigned successfully",
                    "ServiceProviderId": selected_provider.ServiceProviderId,
                    "ProviderName": selected_provider.ProviderName,
                    "AssignmentMode": "random"
                }
            else:
                return {"success": False, "message": "Failed to auto-assign Service Provider"}

        finally:
            await self.db_manager.disconnect()

    async def get_available_providers(self, work_location: str = None, pincode: str = None, service_name: str = None):
        """
        Get all available providers for visible profile booking model.
        """
        try:
            await self.db_manager.connect()

            filters = {
                "IsActive": True,
                "AvailabilityStatus": "available",
                "IsVerified": True
            }

            if work_location:
                filters["WorkLocation"] = work_location

            if pincode:
                filters["Pincode"] = pincode

            if service_name:
                filters["ServiceName"] = service_name

            return await self.db_manager.read(ServiceProvider, filters)

        finally:
            await self.db_manager.disconnect()

    async def update_request_status(self, request_id: int, status: Literal["pending", "assigned", "accepted", "in_progress", "completed", "cancelled", "rejected"]):
        """
        Update the status of a service request with appropriate timestamp.
        """
        try:
            await self.db_manager.connect()

            payload = {
                "Status": status,
                "UpdatedAt": ist_now()
            }

            # Set appropriate timestamp based on status
            if status == "accepted":
                payload["AcceptedAt"] = ist_now()
            elif status == "completed":
                payload["CompletedAt"] = ist_now()
            elif status == "cancelled":
                payload["CancelledAt"] = ist_now()

            updated = await self.db_manager.update(ServiceRequest, {"RequestId": request_id}, payload)

            return {
                "success": bool(updated),
                "message": f"Request status updated to {status}" if updated else "Request not found"
            }

        finally:
            await self.db_manager.disconnect()

    # ------------------------------------------------------
    # Provider-specific methods for "My Services"
    # ------------------------------------------------------
    async def get_service_requests_by_provider(self, provider_id: int, status: str = None):
        """
        Get all service requests assigned to a specific provider.
        Used for 'My Services' dashboard.
        """
        try:
            await self.db_manager.connect()
            filters = {"ServiceProviderId": provider_id}

            if status:
                filters["Status"] = status

            return await self.db_manager.read(ServiceRequest, filters)
        finally:
            await self.db_manager.disconnect()

    async def accept_service_request(self, request_id: int, provider_id: int):
        """
        Provider accepts an assigned service request.
        """
        try:
            await self.db_manager.connect()

            # Verify the request is assigned to this provider
            request = await self.get_service_request_by_id(request_id)
            if not request:
                return {"success": False, "message": "Service request not found"}

            if request.ServiceProviderId != provider_id:
                return {"success": False, "message": "Request not assigned to this provider"}

            if request.Status != "assigned":
                return {"success": False, "message": f"Cannot accept request with status: {request.Status}"}

            payload = {
                "Status": "accepted",
                "AcceptedAt": ist_now(),
                "UpdatedAt": ist_now()
            }

            updated = await self.db_manager.update(ServiceRequest, {"RequestId": request_id}, payload)

            # Trigger notification for provider accepted
            if updated:
                try:
                    await service_request_notifications.notify_provider_accepted(
                        phone_number=request.CustomerPhone,
                        request_id=request_id,
                        provider_name=request.ProviderName if 'provider' in locals() else "Provider",
                        preference=request.NotificationPreference
                    )
                    logger.info(f"Notification triggered for provider accepted on request #{request_id}")
                except Exception as notify_err:
                    logger.warning(f"Failed to send acceptance notification: {notify_err}")

            return {
                "success": bool(updated),
                "message": "Service request accepted" if updated else "Failed to accept request"
            }
        finally:
            await self.db_manager.disconnect()

    async def reject_service_request(self, request_id: int, provider_id: int, provider_notes: str = None):
        """
        Provider rejects an assigned service request.
        """
        try:
            await self.db_manager.connect()

            # Verify the request is assigned to this provider
            request = await self.get_service_request_by_id(request_id)
            if not request:
                return {"success": False, "message": "Service request not found"}

            if request.ServiceProviderId != provider_id:
                return {"success": False, "message": "Request not assigned to this provider"}

            if request.Status not in ["assigned", "accepted"]:
                return {"success": False, "message": f"Cannot reject request with status: {request.Status}"}

            payload = {
                "Status": "rejected",
                "ServiceProviderId": None,  # Unassign the provider
                "ProviderNotes": provider_notes,
                "UpdatedAt": ist_now()
            }

            updated = await self.db_manager.update(ServiceRequest, {"RequestId": request_id}, payload)

            return {
                "success": bool(updated),
                "message": "Service request rejected" if updated else "Failed to reject request"
            }
        finally:
            await self.db_manager.disconnect()

    async def start_service(self, request_id: int, provider_id: int):
        """
        Provider starts the service (changes status to in_progress).
        """
        try:
            await self.db_manager.connect()

            # Verify the request is assigned to this provider
            request = await self.get_service_request_by_id(request_id)
            if not request:
                return {"success": False, "message": "Service request not found"}

            if request.ServiceProviderId != provider_id:
                return {"success": False, "message": "Request not assigned to this provider"}

            if request.Status != "accepted":
                return {"success": False, "message": f"Cannot start service with status: {request.Status}. Must be accepted first."}

            payload = {
                "Status": "in_progress",
                "UpdatedAt": ist_now()
            }

            updated = await self.db_manager.update(ServiceRequest, {"RequestId": request_id}, payload)

            return {
                "success": bool(updated),
                "message": "Service started" if updated else "Failed to start service"
            }
        finally:
            await self.db_manager.disconnect()

    async def complete_service(self, request_id: int, provider_id: int, final_price: float = None):
        """
        Provider completes the service.
        """
        try:
            await self.db_manager.connect()

            # Verify the request is assigned to this provider
            request = await self.get_service_request_by_id(request_id)
            if not request:
                return {"success": False, "message": "Service request not found"}

            if request.ServiceProviderId != provider_id:
                return {"success": False, "message": "Request not assigned to this provider"}

            if request.Status != "in_progress":
                return {"success": False, "message": f"Cannot complete service with status: {request.Status}. Must be in_progress first."}

            payload = {
                "Status": "completed",
                "CompletedAt": ist_now(),
                "UpdatedAt": ist_now()
            }

            if final_price is not None:
                payload["FinalPrice"] = final_price

            updated = await self.db_manager.update(ServiceRequest, {"RequestId": request_id}, payload)

            # Trigger notification for service completed
            if updated:
                try:
                    await service_request_notifications.notify_service_completed(
                        phone_number=request.CustomerPhone,
                        request_id=request_id,
                        provider_name=request.ProviderName if hasattr(request, 'ProviderName') else "Provider",
                        final_price=final_price,
                        preference=request.NotificationPreference
                    )
                    logger.info(f"Notification triggered for service completed on request #{request_id}")
                except Exception as notify_err:
                    logger.warning(f"Failed to send completion notification: {notify_err}")

            return {
                "success": bool(updated),
                "message": "Service completed" if updated else "Failed to complete service"
            }
        finally:
            await self.db_manager.disconnect()

    async def update_provider_notes(self, request_id: int, provider_id: int, provider_notes: str):
        """
        Update provider notes for a service request.
        """
        try:
            await self.db_manager.connect()

            # Verify the request is assigned to this provider
            request = await self.get_service_request_by_id(request_id)
            if not request:
                return {"success": False, "message": "Service request not found"}

            if request.ServiceProviderId != provider_id:
                return {"success": False, "message": "Request not assigned to this provider"}

            payload = {
                "ProviderNotes": provider_notes,
                "UpdatedAt": ist_now()
            }

            updated = await self.db_manager.update(ServiceRequest, {"RequestId": request_id}, payload)

            return {
                "success": bool(updated),
                "message": "Provider notes updated" if updated else "Failed to update notes"
            }
        finally:
            await self.db_manager.disconnect()
