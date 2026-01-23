import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from ...config import settings
from ...crud.customer.lap_manager import (
    LabManager, TestManager, AppointmentManager,
    LabCreate, LabUpdate,
    TestCreate, TestUpdate,
    AppointmentCreate, AppointmentUpdate
)
from ...utils.image_uploader import save_picture



# ============================================
# LabAPI
# ============================================
class LabAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = LabManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/labs")(self.create_lab)
        self.router.get("/labs")(self.get_labs)
        self.router.get("/labs/{lab_id}")(self.get_lab_by_id)
        self.router.get("/labs/postal/{postal}")(self.get_labs_by_postal)
        self.router.put("/labs/{lab_id}")(self.update_lab)
        self.router.delete("/labs/{lab_id}")(self.delete_lab)

    async def create_lab(
        self,
        Name: str = Form(...),
        Contact: str = Form(None),
        Email: str = Form(None),
        Timings: str = Form(None),
        Reviews: str = Form(None),
        AddressLine1: str = Form(None),
        AddressLine2: str = Form(None),
        City: str = Form(None),
        State: str = Form(None),
        Country: str = Form(None),
        PostalCode: str = Form(None),
        Latitude: str = Form(None),
        Longitude: str = Form(None),
        ShopPic: UploadFile = File(None)
    ):
        try:
            img_path = await save_picture(ShopPic, "Lab") if ShopPic else None
            obj = LabCreate(
                Name=Name,
                Contact=Contact,
                Email=Email,
                Timings=Timings,
                Reviews=Reviews,
                AddressLine1=AddressLine1,
                AddressLine2=AddressLine2,
                City=City,
                State=State,
                Country=Country,
                PostalCode=PostalCode,
                Latitude=Latitude,
                Longitude=Longitude,
                ShopPic=img_path
            )
            return await self.manager.create_lab(obj)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_labs(self):
        return await self.manager.get_labs()

    async def get_lab_by_id(self, lab_id: int):
        lab = await self.manager.get_lab_by_id(lab_id)
        if not lab:
            raise HTTPException(status_code=404, detail="Lab not found")
        return lab

    async def get_labs_by_postal(self, postal: str):
        return await self.manager.get_labs_by_postal(postal)

    async def update_lab(
        self,
        lab_id: int,
        Name: str = Form(None),
        Contact: str = Form(None),
        Email: str = Form(None),
        Timings: str = Form(None),
        Reviews: str = Form(None),
        AddressLine1: str = Form(None),
        AddressLine2: str = Form(None),
        City: str = Form(None),
        State: str = Form(None),
        Country: str = Form(None),
        PostalCode: str = Form(None),
        Latitude: str = Form(None),
        Longitude: str = Form(None),
        ShopPic: UploadFile = File(None)
    ):
        try:
            old_data = await self.manager.get_lab_by_id(lab_id)
            if not old_data:
                raise HTTPException(status_code=404, detail="Lab not found")

            update_data = {}
            for field_name, value in {
                "Name": Name,
                "Contact": Contact,
                "Email": Email,
                "Timings": Timings,
                "Reviews": Reviews,
                "AddressLine1": AddressLine1,
                "AddressLine2": AddressLine2,
                "City": City,
                "State": State,
                "Country": Country,
                "PostalCode": PostalCode,
                "Latitude": Latitude,
                "Longitude": Longitude
            }.items():
                if value is not None:
                    update_data[field_name] = value

            if ShopPic:
                new_path = await save_picture(ShopPic, "Lab")
                old_path = old_data.ShopPic
                if old_path:
                    abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_path))
                    if os.path.exists(abs_old_path):
                        os.remove(abs_old_path)
                update_data["ShopPic"] = new_path

            return await self.manager.update_lab(lab_id, LabUpdate(**update_data))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_lab(self, lab_id: int):
        try:
            old_data = await self.manager.get_lab_by_id(lab_id)
            if old_data and old_data.ShopPic:
                abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_data.ShopPic))
                if os.path.exists(abs_old_path):
                    os.remove(abs_old_path)
            return await self.manager.delete_lab(lab_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))




# ============================================
# TEST API
# ============================================
class TestAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = TestManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/tests")(self.create_test)
        self.router.get("/tests/{test_id}")(self.get_test_by_id)
        self.router.get("/tests/lab/{lab_id}")(self.get_tests_by_lab)
        self.router.put("/tests/{test_id}")(self.update_test)
        self.router.delete("/tests/{test_id}")(self.delete_test)

    async def create_test(self, data: TestCreate):
        return await self.manager.create_test(data)

    async def get_test_by_id(self, test_id: int):
        return await self.manager.get_test_by_id(test_id)

    async def get_tests_by_lab(self, lab_id: int):
        return await self.manager.get_tests_by_lab(lab_id)

    async def update_test(self, test_id: int, data: TestUpdate):
        return await self.manager.update_test(test_id, data)

    async def delete_test(self, test_id: int):
        return await self.manager.delete_test(test_id)


# ============================================
# APPOINTMENT API
# ============================================
class AppointmentAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = AppointmentManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/appointments")(self.create_appointment)
        self.router.get("/appointments/{appointment_id}")(self.get_appt_by_id)
        self.router.get("/appointments/lab/{lab_id}")(self.get_appts_by_lab)
        self.router.put("/appointments/{appointment_id}")(self.update_appt)
        self.router.delete("/appointments/{appointment_id}")(self.delete_appt)

    async def create_appointment(self, data: AppointmentCreate):
        return await self.manager.create_appointment(data)

    async def get_appt_by_id(self, appointment_id: int):
        return await self.manager.get_appointment_by_id(appointment_id)

    async def get_appts_by_lab(self, lab_id: int):
        return await self.manager.get_appointments_by_lab(lab_id)

    async def update_appt(self, appointment_id: int, data: AppointmentUpdate):
        return await self.manager.update_appointment(appointment_id, data)

    async def delete_appt(self, appointment_id: int):
        return await self.manager.delete_appointment(appointment_id)
