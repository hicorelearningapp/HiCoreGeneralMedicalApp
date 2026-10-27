from ...utils.logger import get_logger
from ...db.base.database_manager import DatabaseManager
from ...models.customer.service_request_model import ServiceRequest
from ...models.customer.service_provider_model import ServiceProvider
from ...models.customer.service_list_model import ServiceList
from ...models.customer.provider_services_model import ProviderServices

from ...schemas.customer.service_request_schema import (
    ServiceRequestCreate,
    ServiceRequestUpdate,
    ServiceRequestRead
)

logger = get_logger(__name__)


class ServiceRequestManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    # -------------------------------
    # ATTACH FULL DETAILS
    # -------------------------------
    async def _attach_full_details(self, request_obj):
        data = ServiceRequestRead.from_orm(request_obj).dict()

        # Provider
        provider_data = None
        if request_obj.ServiceProviderId:
            provider = await self.db_manager.read(
                ServiceProvider,
                {"ServiceProviderId": request_obj.ServiceProviderId}
            )
            if provider:
                p = provider[0]
                provider_data = {
                    "ProviderName": p.ProviderName,
                    "Address": p.Address,
                    "Pincode": p.Pincode,
                    "PhoneNumber": p.PhoneNumber,
                    "Email": p.Email,
                    "ExperienceYears": p.ExperienceYears,
                    "Rating": p.Rating,
                }

        # ServiceList
        service_data = None
        if request_obj.ServiceListId:
            service = await self.db_manager.read(
                ServiceList,
                {"ServiceListId": request_obj.ServiceListId}
            )
            if service:
                s = service[0]
                service_data = {
                    "ServiceName": s.ServiceName,
                    "Description": s.Description,
                    "Price": s.Price,
                    "DurationMinutes": s.DurationMinutes,
                }

        # ProviderServices
        provider_service_data = None
        if request_obj.ProviderServiceId:
            ps = await self.db_manager.read(
                ProviderServices,
                {"ProviderServiceId": request_obj.ProviderServiceId}
            )
            if ps:
                p = ps[0]
                provider_service_data = {
                    "Price": p.Price,
                    "DurationMinutes": p.DurationMinutes,
                    "ServiceListId": p.ServiceListId,
                    "ServiceProviderId": p.ServiceProviderId
                }

        data["ProviderInfo"] = provider_data
        data["ServiceInfo"] = service_data
        data["ProviderServiceInfo"] = provider_service_data

        return data

    # -------------------------------
    # CREATE
    # -------------------------------
    async def create(self, payload: ServiceRequestCreate):
        try:
            await self.db_manager.connect()
            obj = await self.db_manager.create(ServiceRequest, payload.dict())

            return {
                "success": True,
                "message": "Request created",
                "data": await self._attach_full_details(obj)
            }

        except Exception as e:
            logger.error(e)
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # GET SINGLE
    # -------------------------------
    async def get(self, id: int):
        try:
            await self.db_manager.connect()

            result = await self.db_manager.read(ServiceRequest, {"ServiceRequestId": id})

            if result:
                return {
                    "success": True,
                    "message": "Fetched",
                    "data": await self._attach_full_details(result[0])
                }

            return {"success": False, "message": "Not found", "data": None}

        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # GET ALL
    # -------------------------------
    async def get_all(self):
        try:
            await self.db_manager.connect()

            result = await self.db_manager.read(ServiceRequest)

            data = []
            for r in result:
                data.append(await self._attach_full_details(r))

            return {"success": True, "message": "Fetched", "data": data}

        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # UPDATE
    # -------------------------------
    async def update(self, id: int, payload: ServiceRequestUpdate):
        try:
            await self.db_manager.connect()

            update_data = payload.dict(exclude_unset=True)

            rowcount = await self.db_manager.update(
                ServiceRequest,
                {"ServiceRequestId": id},
                update_data
            )

            return {
                "success": bool(rowcount),
                "message": "Updated" if rowcount else "No changes",
                "data": {"rows_affected": rowcount}
            }

        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # DELETE
    # -------------------------------
    async def delete(self, id: int):
        try:
            await self.db_manager.connect()

            rowcount = await self.db_manager.delete(
                ServiceRequest,
                {"ServiceRequestId": id}
            )

            return {
                "success": bool(rowcount),
                "message": "Deleted" if rowcount else "Not found",
                "data": {"rows_affected": rowcount}
            }

        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # UPDATE STATUS
    # -------------------------------
    async def update_status(self, id: int, status: str):
        try:
            await self.db_manager.connect()

            rowcount = await self.db_manager.update(
                ServiceRequest,
                {"ServiceRequestId": id},
                {"Status": status}
            )

            return {
                "success": bool(rowcount),
                "message": f"Status updated to {status}",
                "data": {"rows_affected": rowcount}
            }

        finally:
            await self.db_manager.disconnect()

    # -------------------------------
    # GET BY PROVIDER
    # -------------------------------
    async def get_by_provider(self, provider_id: int):
        await self.db_manager.connect()

        result = await self.db_manager.read(
            ServiceRequest,
            {"ServiceProviderId": provider_id}
        )

        data = [await self._attach_full_details(r) for r in result]

        return {"success": True, "message": "Provider requests", "data": data}

    # -------------------------------
    # GET BY CUSTOMER
    # -------------------------------
    async def get_by_customer(self, customer_id: int):
        await self.db_manager.connect()

        result = await self.db_manager.read(
            ServiceRequest,
            {"CustomerId": customer_id}
        )

        data = [await self._attach_full_details(r) for r in result]

        return {"success": True, "message": "Customer requests", "data": data}

    # -------------------------------
    # AUTO ASSIGN (SMART)
    # -------------------------------
    async def auto_assign(self, pincode: str, service_list_id: int):
        try:
            await self.db_manager.connect()

            providers = await self.db_manager.read(
                ServiceProvider,
                {"Pincode": pincode}
            )

            matched = []

            for provider in providers:
                check = await self.db_manager.read(
                    ProviderServices,
                    {
                        "ServiceProviderId": provider.ServiceProviderId,
                        "ServiceListId": service_list_id
                    }
                )

                if check:
                    matched.append({
                        "ServiceProviderId": provider.ServiceProviderId,
                        "ProviderName": provider.ProviderName,
                        "PhoneNumber": provider.PhoneNumber,
                        "Pincode": provider.Pincode
                    })

            if not matched:
                return {"success": False, "message": "No matching provider"}

            return {
                "success": True,
                "message": "Auto assigned",
                "data": matched[0],
                "all": matched
            }

        finally:
            await self.db_manager.disconnect()