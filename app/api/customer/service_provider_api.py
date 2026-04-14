import os
from fastapi import APIRouter, HTTPException, Form, File, UploadFile

from ...config import settings
from ...crud.customer.service_provider_manager import ServiceProviderManager
from ...schemas.customer.service_provider_schema import (
    ServiceProviderCreate,
    ServiceProviderUpdate,
    ProviderRegisterSchema,
    ProviderLoginSchema
)
from ...utils.image_uploader import save_picture


class ServiceProviderAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = ServiceProviderManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/providers/register", response_model=dict)(self.register)
        self.router.post("/providers/login", response_model=dict)(self.login)
        self.router.post("/providers", response_model=dict)(self.create_provider)
        self.router.get("/providers/{provider_id}", response_model=dict)(self.get_provider)
        self.router.get("/providers", response_model=dict)(self.get_all_providers)
        self.router.put("/providers/{provider_id}", response_model=dict)(self.update_provider)
        self.router.delete("/providers/{provider_id}", response_model=dict)(self.delete_provider)

    # -------------------------------
    # CREATE PROVIDER
    # -------------------------------
    async def create_provider(
        self,
        ProviderName: str = Form(None),
        Email: str = Form(None),
        Password: str = Form(None),
        PhoneNumber: str = Form(None),
        PhotoUrl: UploadFile = File(None),
        Address: str = Form(None),
        Pincode: str = Form(None),
        ExperienceYears: int = Form(None),
        Gender: str = Form(None),
        DateOfBirth: str = Form(None),
        AvailabilityStatus: str = Form(None),
        Rating: float = Form(None),
        Specialization: str = Form(None),
        ServiceDescription: str = Form(None),
    ):
        try:
            # Save image
            photo_path = await save_picture(PhotoUrl, "Provider")

            provider_obj = ServiceProviderCreate(
                ProviderName=ProviderName,
                Email=Email,
                Password=Password,
                PhoneNumber=PhoneNumber,
                PhotoUrl=photo_path,
                Address=Address,
                Pincode=Pincode,
                ExperienceYears=ExperienceYears,
                Gender=Gender,
                DateOfBirth=DateOfBirth,
                AvailabilityStatus=AvailabilityStatus,
                Rating=Rating,
                Specialization=Specialization,
                ServiceDescription=ServiceDescription,
            )

            return await self.crud.create_provider(provider_obj)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # GET SINGLE
    # -------------------------------
    async def get_provider(self, provider_id: int):
        try:
            return await self.crud.get_provider(provider_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # GET ALL
    # -------------------------------
    async def get_all_providers(self):
        try:
            return await self.crud.get_all_providers()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # UPDATE PROVIDER (FULL FIXED)
    # -------------------------------
    async def update_provider(
        self,
        provider_id: int,
        ProviderName: str = Form(None),
        Email: str = Form(None),
        Password: str = Form(None),
        PhoneNumber: str = Form(None),
        Address: str = Form(None),
        Pincode: str = Form(None),
        ExperienceYears: int = Form(None),
        Gender: str = Form(None),
        DateOfBirth: str = Form(None),
        AvailabilityStatus: str = Form(None),
        Rating: float = Form(None),
        Specialization: str = Form(None),
        ServiceDescription: str = Form(None),
        PhotoUrl: UploadFile = File(None),
    ):
        try:
            # Get existing provider
            old_provider = await self.crud.get_provider(provider_id)
            if not old_provider["success"]:
                raise HTTPException(status_code=404, detail="Provider not found")

            update_data = {}

            # Handle normal fields
            for field_name, value in {
                "ProviderName": ProviderName,
                "Email": Email,
                "Password": Password,
                "PhoneNumber": PhoneNumber,
                "Address": Address,
                "Pincode": Pincode,
                "ExperienceYears": ExperienceYears,
                "Gender": Gender,
                "DateOfBirth": DateOfBirth,
                "AvailabilityStatus": AvailabilityStatus,
                "Rating": Rating,
                "Specialization": Specialization,
                "ServiceDescription": ServiceDescription,
            }.items():
                if value is not None:
                    update_data[field_name] = value

            # Handle image update
            if PhotoUrl:
                new_path = await save_picture(PhotoUrl, "Provider")

                old_path = old_provider["data"]["PhotoUrl"]

                if old_path:
                    abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_path))

                    if os.path.exists(abs_old_path):
                        os.remove(abs_old_path)
                        print(f"Deleted old image: {abs_old_path}")
                    else:
                        print(f"Old image not found: {abs_old_path}")

                update_data["PhotoUrl"] = new_path

            return await self.crud.update_provider(
                provider_id,
                ServiceProviderUpdate(**update_data)
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # DELETE PROVIDER
    # -------------------------------
    async def delete_provider(self, provider_id: int):
        try:
            provider = await self.crud.get_provider(provider_id)
            if not provider["success"]:
                raise HTTPException(status_code=404, detail="Provider not found")

            image_path = provider["data"]["PhotoUrl"]

            result = await self.crud.delete_provider(provider_id)

            # Delete image file
            if image_path:
                abs_path = os.path.normpath(os.path.join(os.getcwd(), image_path))

                print("Deleting:", abs_path)

                if os.path.exists(abs_path):
                    os.remove(abs_path)
                else:
                    print("File does not exist:", abs_path)

            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # REGISTER
    # -------------------------------
    async def register(self, payload: ProviderRegisterSchema):
        result = await self.crud.register(payload.Email, payload.Password)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result

    # -------------------------------
    # LOGIN
    # -------------------------------
    async def login(self, payload: ProviderLoginSchema):
        result = await self.crud.login(payload.Email, payload.Password)
        if not result["success"]:
            raise HTTPException(status_code=401, detail=result["message"])
        return result