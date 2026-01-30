import os
from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from ...config import settings
from ...crud.customer.medicine_manager import (
    MedicalTypeManager,
    MedicineCategoryManager,
    MedicineManager,
    MedicineInfoManager
)
from ...schemas.customer.medicine_schema import (
    MedicalTypeCreate,
    MedicalTypeUpdate,
    MedicineCategoryCreate,
    MedicineCategoryUpdate,
    MedicineCreate,
    MedicineUpdate,
    MedicineInfoCreate,
    MedicineInfoUpdate
)
from ...utils.image_uploader import save_picture


# -------------------------------
# MedicalTypeAPI
# -------------------------------
class MedicalTypeAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = MedicalTypeManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/medicine-types")(self.create_medicine_type)
        self.router.get("/medicine-types")(self.get_medicine_types)
        self.router.put("/medicine-types/{medicine_type_id}")(self.update_medicine_type)
        self.router.delete("/medicine-types/{medicine_type_id}")(self.delete_medicine_type)

    async def create_medicine_type(
        self,
        MedicalType: str = Form(...),
        ImgUrl: UploadFile = File(None)
    ):
        try:
            img_path = await save_picture(ImgUrl, "MedicalType") if ImgUrl else None
            obj = MedicalTypeCreate(MedicalType=MedicalType, ImgUrl=img_path)
            return await self.crud.create_medicine_type(obj)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_medicine_types(self):
        return await self.crud.get_medicine_types()

    async def update_medicine_type(
        self,
        medicine_type_id: int,
        MedicalType: str = Form(None),
        ImgUrl: UploadFile = File(None)
    ):
        try:
            old_data = await self.crud.get_medicine_types(filters={"MedicalTypeId": medicine_type_id})
            if not old_data:
                raise HTTPException(status_code=404, detail="MedicalType not found")

            update_data = {}
            if MedicalType is not None:
                update_data["MedicalType"] = MedicalType

            if ImgUrl:
                new_path = await save_picture(ImgUrl, "MedicalType")
                old_path = old_data[0].ImgUrl
                if old_path:
                    abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_path))
                    if os.path.exists(abs_old_path):
                        os.remove(abs_old_path)
                update_data["ImgUrl"] = new_path

            return await self.crud.update_medicine_type(medicine_type_id, MedicalTypeUpdate(**update_data))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_medicine_type(self, medicine_type_id: int):
        try:
            old_data = await self.crud.get_medicine_types(filters={"MedicalTypeId": medicine_type_id})
            if old_data and old_data[0].ImgUrl:
                abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_data[0].ImgUrl))
                if os.path.exists(abs_old_path):
                    os.remove(abs_old_path)
            return await self.crud.delete_medicine_type(medicine_type_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# MedicineCategoryAPI
# -------------------------------
class MedicineCategoryAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = MedicineCategoryManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/medicine-categories")(self.create_medicine_category)
        self.router.get("/medicine-categories")(self.get_medicine_categories)
        self.router.get("/medicine-categories/by-type/{medicine_type_id}")(self.get_categories_by_type)
        self.router.put("/medicine-categories/{medicine_category_id}")(self.update_medicine_category)
        self.router.delete("/medicine-categories/{medicine_category_id}")(self.delete_medicine_category)

    async def create_medicine_category(
        self,
        MedicalTypeId: int = Form(...),
        Category: str = Form(...),
        ImgUrl: UploadFile = File(None)
    ):
        try:
            img_path = await save_picture(ImgUrl, "MedicineCategory") if ImgUrl else None
            obj = MedicineCategoryCreate(MedicalTypeId=MedicalTypeId, Category=Category, ImgUrl=img_path)
            return await self.crud.create_medicine_category(obj)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_medicine_categories(self):
        return await self.crud.get_medicine_categories()

    async def get_categories_by_type(self, medicine_type_id: int):
        return await self.crud.get_categories_by_type(medicine_type_id)

    async def update_medicine_category(
        self,
        medicine_category_id: int,
        MedicalTypeId: int = Form(None),
        Category: str = Form(None),
        ImgUrl: UploadFile = File(None)
    ):
        try:
            old_data = await self.crud.get_medicine_categories(filters={"MedicineCategoryId": medicine_category_id})
            if not old_data:
                raise HTTPException(status_code=404, detail="MedicineCategory not found")

            update_data = {}
            if MedicalTypeId is not None:
                update_data["MedicalTypeId"] = MedicalTypeId
            if Category is not None:
                update_data["Category"] = Category

            if ImgUrl:
                new_path = await save_picture(ImgUrl, "MedicineCategory")
                old_path = old_data[0].ImgUrl
                if old_path:
                    abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_path))
                    if os.path.exists(abs_old_path):
                        os.remove(abs_old_path)
                update_data["ImgUrl"] = new_path

            return await self.crud.update_medicine_category(medicine_category_id, MedicineCategoryUpdate(**update_data))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_medicine_category(self, medicine_category_id: int):
        try:
            old_data = await self.crud.get_medicine_categories(filters={"MedicineCategoryId": medicine_category_id})
            if old_data and old_data[0].ImgUrl:
                abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_data[0].ImgUrl))
                if os.path.exists(abs_old_path):
                    os.remove(abs_old_path)
            return await self.crud.delete_medicine_category(medicine_category_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# MedicineAPI
# -------------------------------
class MedicineAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = MedicineManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/medicines")(self.create_medicine)
        self.router.get("/medicines")(self.get_medicines)
        self.router.get("/medicines/by-category/{category}")(self.get_medicines_by_category)
        self.router.put("/medicines/{medicine_id}")(self.update_medicine)
        self.router.delete("/medicines/{medicine_id}")(self.delete_medicine)

    async def create_medicine(
        self,
        MedicineCategoryId: int = Form(None),
        MedicalTypeId: int = Form(None),
        Name: str = Form(...),
        GenericName: str = Form(None),
        DosageForm: str = Form(None),
        Strength: str = Form(None),
        Manufacturer: str = Form(None),
        PrescriptionRequired: bool = Form(False),
        Size: str = Form(None),
        UnitPrice: float = Form(...),
        TherapeuticClass: str = Form(None),        
        ImgUrl: UploadFile = File(None)
    ):
        try:
            img_path = await save_picture(ImgUrl, "Medicine") if ImgUrl else None
            obj = MedicineCreate(
                MedicineCategoryId=MedicineCategoryId,
                MedicalTypeId=MedicalTypeId,
                Name=Name,
                GenericName=GenericName,
                DosageForm=DosageForm,
                Strength=Strength,
                Manufacturer=Manufacturer,
                PrescriptionRequired=PrescriptionRequired,
                Size=Size,
                UnitPrice=UnitPrice,
                TherapeuticClass=TherapeuticClass,
                ImgUrl=img_path
            )
            return await self.crud.create_medicine(obj)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_medicines(self):
        return await self.crud.get_medicines()

    async def get_medicines_by_category(self, MedicineCategoryId: int):
        return await self.crud.get_medicines_by_category(MedicineCategoryId)

    async def update_medicine(
        self,
        medicine_id: int,
        MedicineCategoryId: int = Form(None),
        MedicalTypeId: int = Form(None),
        Name: str = Form(None),
        GenericName: str = Form(None),
        DosageForm: str = Form(None),
        Strength: str = Form(None),
        Manufacturer: str = Form(None),
        PrescriptionRequired: bool = Form(None),
        Size: str = Form(None),
        UnitPrice: float = Form(None),
        TherapeuticClass: str = Form(None),
        ImgUrl: UploadFile = File(None)
    ):
        try:
            old_data = await self.crud.get_medicines(filters={"MedicineId": medicine_id})
            if not old_data:
                raise HTTPException(status_code=404, detail="Medicine not found")

            update_data = {}
            for field_name, value in {
                "MedicineCategoryId": MedicineCategoryId,
                "MedicalTypeId": MedicalTypeId,
                "Name": Name,
                "GenericName": GenericName,
                "DosageForm": DosageForm,
                "Strength": Strength,
                "Manufacturer": Manufacturer,
                "PrescriptionRequired": PrescriptionRequired,
                "Size": Size,
                "UnitPrice": UnitPrice,
                "TherapeuticClass": TherapeuticClass
            }.items():
                if value is not None:
                    update_data[field_name] = value

            if ImgUrl:
                new_path = await save_picture(ImgUrl, "Medicine")
                old_path = old_data[0].ImgUrl
                if old_path:
                    abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_path))
                    if os.path.exists(abs_old_path):
                        os.remove(abs_old_path)
                update_data["ImgUrl"] = new_path

            return await self.crud.update_medicine(medicine_id, MedicineUpdate(**update_data))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_medicine(self, medicine_id: int):
        try:
            old_data = await self.crud.get_medicines(filters={"MedicineId": medicine_id})
            if old_data and old_data[0].ImgUrl:
                abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_data[0].ImgUrl))
                if os.path.exists(abs_old_path):
                    os.remove(abs_old_path)
            return await self.crud.delete_medicine(medicine_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))




# ============================================================
# MedicineInfoAPI
# ============================================================
class MedicineInfoAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = MedicineInfoManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/medicine-infos")(self.create_medicine_info)
        self.router.get("/medicine-infos")(self.get_medicine_infos)
        self.router.get("/medicine-infos/by-medicine/{medicine_id}")(self.get_infos_by_medicine_id)
        self.router.put("/medicine-infos/{medicine_info_id}")(self.update_medicine_info)
        self.router.delete("/medicine-infos/{medicine_info_id}")(self.delete_medicine_info)

    async def create_medicine_info(self, data: MedicineInfoCreate):
        return await self.crud.create_medicine_info(data)

    async def get_medicine_infos(self):
        return await self.crud.get_medicine_infos()

    async def get_infos_by_medicine_id(self, medicine_id: int):
        return await self.crud.get_infos_by_medicine_id(medicine_id)

    async def update_medicine_info(self, medicine_info_id: int, data: MedicineInfoUpdate):
        return await self.crud.update_medicine_info(medicine_info_id, data)

    async def delete_medicine_info(self, medicine_info_id: int):
        return await self.crud.delete_medicine_info(medicine_info_id)
