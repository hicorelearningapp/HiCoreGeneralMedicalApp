import os
from typing import Literal
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
from ...config import settings
from ...crud.customer.service_provider_manager import (
    ServiceProviderManager,
    ServiceProviderCreate, ServiceProviderUpdate
)
from ...utils.image_uploader import save_picture


# --------------------------------------------------
# Service Provider API
# --------------------------------------------------
class ServiceProviderAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = ServiceProviderManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/service-providers")(self.create_service_provider)
        self.router.get("/service-providers")(self.get_service_providers)
        self.router.get("/service-providers/{service_provider_id}")(self.get_service_provider_by_id)
        self.router.put("/service-providers/{service_provider_id}")(self.update_service_provider)
        self.router.delete("/service-providers/{service_provider_id}")(self.delete_service_provider)

    async def create_service_provider(
        self,
        ProviderName: str = Form(...),
        Address: str = Form(...),
        Pincode: str = Form(...),
        PhoneNumber: str = Form(...),
        Email: str = Form(...),
        ExperienceYears: int = Form(...),
        Gender: str = Form(...),
        DateOfBirth: str = Form(...),
        LicenseNumber: str = Form(None),
        AvailabilityStatus: Literal["available", "unavailable", "busy"] = Form("available"),
        Rating: float = Form(0.0),
        IsVerified: bool = Form(False),
        IsActive: bool = Form(True),
        Specialization: str = Form(...),
        ServiceDescription: str = Form(...),
        ServiceCategory: str = Form(...),
        ServicesOffered: str = Form(None),
        ProfileCompleted: bool = Form(False),
        Photo: UploadFile = File(None),
        Certificate: UploadFile = File(None),
        AadhaarOrIdProof: UploadFile = File(None)
    ):
        try:
            photo_path = await save_picture(Photo, "ServiceProvider") if Photo else None
            certificate_path = await save_picture(Certificate, "ServiceProvider") if Certificate else None
            id_proof_path = await save_picture(AadhaarOrIdProof, "ServiceProvider") if AadhaarOrIdProof else None

            obj = ServiceProviderCreate(
                ProviderName=ProviderName,
                PhotoUrl=photo_path,
                CertificateUrl=certificate_path,
                AadhaarOrIdProofUrl=id_proof_path,
                Address=Address,
                Pincode=Pincode,
                PhoneNumber=PhoneNumber,
                Email=Email,
                ExperienceYears=ExperienceYears,
                Gender=Gender,
                DateOfBirth=DateOfBirth,
                LicenseNumber=LicenseNumber,
                AvailabilityStatus=AvailabilityStatus,
                Rating=Rating,
                IsVerified=IsVerified,
                IsActive=IsActive,
                Specialization=Specialization,
                ServiceDescription=ServiceDescription,
                ServiceCategory=ServiceCategory,
                ServicesOffered=ServicesOffered,
                ProfileCompleted=ProfileCompleted
            )
            return await self.manager.create_service_provider(obj)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_service_providers(
        self,
        service_name: str = Query(None),
        pincode: str = Query(None),
        availability_status: Literal["available", "unavailable", "busy"] = Query(None),
        is_verified: bool = Query(None)
    ):
        try:
            return await self.manager.get_service_providers(
                service_name=service_name,
                pincode=pincode,
                availability_status=availability_status,
                is_verified=is_verified
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_service_provider_by_id(self, service_provider_id: int):
        provider = await self.manager.get_service_provider_by_id(service_provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="Service Provider not found")
        return provider

    async def update_service_provider(
        self,
        service_provider_id: int,
        ProviderName: str = Form(None),
        Address: str = Form(None),
        Pincode: str = Form(None),
        PhoneNumber: str = Form(None),
        Email: str = Form(None),
        ExperienceYears: int = Form(None),
        Gender: str = Form(None),
        DateOfBirth: str = Form(None),
        LicenseNumber: str = Form(None),
        AvailabilityStatus: Literal["available", "unavailable", "busy"] = Form(None),
        Rating: float = Form(None),
        IsVerified: bool = Form(None),
        IsActive: bool = Form(None),
        Specialization: str = Form(None),
        ServiceDescription: str = Form(None),
        ServiceCategory: str = Form(None),
        ServicesOffered: str = Form(None),
        ProfileCompleted: bool = Form(False),
        Photo: UploadFile = File(None),
        Certificate: UploadFile = File(None),
        AadhaarOrIdProof: UploadFile = File(None)
    ):
        try:
            old_data = await self.manager.get_service_provider_by_id(service_provider_id)
            if not old_data:
                raise HTTPException(status_code=404, detail="Service Provider not found")

            update_data = {}
            for field_name, value in {
                "ProviderName": ProviderName,
                "Address": Address,
                "Pincode": Pincode,
                "PhoneNumber": PhoneNumber,
                "Email": Email,
                "ExperienceYears": ExperienceYears,
                "Gender": Gender,
                "DateOfBirth": DateOfBirth,
                "LicenseNumber": LicenseNumber,
                "AvailabilityStatus": AvailabilityStatus,
                "Rating": Rating,
                "IsVerified": IsVerified,
                "IsActive": IsActive,
                "Specialization": Specialization,
                "ServiceDescription": ServiceDescription,
                "ServiceCategory": ServiceCategory,
                "ServicesOffered": ServicesOffered,
                "ProfileCompleted": ProfileCompleted
            }.items():
                if value is not None:
                    update_data[field_name] = value

            # Handle file uploads
            if Photo:
                new_path = await save_picture(Photo, "ServiceProvider")
                old_path = old_data.PhotoUrl
                if old_path:
                    abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_path))
                    if os.path.exists(abs_old_path):
                        os.remove(abs_old_path)
                update_data["PhotoUrl"] = new_path

            if Certificate:
                new_path = await save_picture(Certificate, "ServiceProvider")
                old_path = old_data.CertificateUrl
                if old_path:
                    abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_path))
                    if os.path.exists(abs_old_path):
                        os.remove(abs_old_path)
                update_data["CertificateUrl"] = new_path

            if AadhaarOrIdProof:
                new_path = await save_picture(AadhaarOrIdProof, "ServiceProvider")
                old_path = old_data.AadhaarOrIdProofUrl
                if old_path:
                    abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_path))
                    if os.path.exists(abs_old_path):
                        os.remove(abs_old_path)
                update_data["AadhaarOrIdProofUrl"] = new_path

            return await self.manager.update_service_provider(service_provider_id, ServiceProviderUpdate(**update_data))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_service_provider(self, service_provider_id: int):
        try:
            old_data = await self.manager.get_service_provider_by_id(service_provider_id)
            if old_data:
                # Delete associated files
                for file_path in [old_data.PhotoUrl, old_data.CertificateUrl, old_data.AadhaarOrIdProofUrl]:
                    if file_path:
                        abs_path = os.path.normpath(os.path.join(os.getcwd(), file_path))
                        if os.path.exists(abs_path):
                            os.remove(abs_path)
            return await self.manager.delete_service_provider(service_provider_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
