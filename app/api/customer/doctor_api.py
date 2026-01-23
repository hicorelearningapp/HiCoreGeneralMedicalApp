import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from ...config import settings
from ...crud.customer.doctor_manager import (
    DoctorManager, DoctorAppointmentManager,
    DoctorCreate, DoctorUpdate,
    DoctorAppointmentCreate, DoctorAppointmentUpdate
)
from ...utils.image_uploader import save_picture

# --------------------------------------------------
# DoctorAPI
# --------------------------------------------------
class DoctorAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = DoctorManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/doctors")(self.create_doctor)
        self.router.get("/doctors")(self.get_doctors)
        self.router.get("/doctors/{doctor_id}")(self.get_doctor_by_id)
        self.router.put("/doctors/{doctor_id}")(self.update_doctor)
        self.router.delete("/doctors/{doctor_id}")(self.delete_doctor)

    async def create_doctor(
        self,
        FirstName: str = Form(...),
        LastName: str = Form(...),
        Gender: str = Form(None),
        DateOfBirth: str = Form(None),
        Email: str = Form(None),
        MobileNumber: str = Form(None),
        Specialization: str = Form(None),
        Qualifications: str = Form(None),
        ExperienceYears: int = Form(None),
        LicenseNumber: str = Form(None),
        ClinicName: str = Form(None),
        ClinicAddress: str = Form(None),
        City: str = Form(None),
        State: str = Form(None),
        Country: str = Form(None),
        PostalCode: str = Form(None),
        ConsultationFee: float = Form(0.0),
        AvailableDays: str = Form(None),
        AvailableTime: str = Form(None),
        SlotDurationMinutes: int = Form(None),
        About: str = Form(None),
        Reviews: str = Form(None),
        Status: str = Form(None),
        ProfilePhoto: UploadFile = File(None)
    ):
        try:
            img_path = await save_picture(ProfilePhoto, "Doctor") if ProfilePhoto else None
            obj = DoctorCreate(
                FirstName=FirstName,
                LastName=LastName,
                Gender=Gender,
                DateOfBirth=DateOfBirth,
                Email=Email,
                MobileNumber=MobileNumber,
                Specialization=Specialization,
                Qualifications=Qualifications,
                ExperienceYears=ExperienceYears,
                LicenseNumber=LicenseNumber,
                ClinicName=ClinicName,
                ClinicAddress=ClinicAddress,
                City=City,
                State=State,
                Country=Country,
                PostalCode=PostalCode,
                ConsultationFee=ConsultationFee,
                AvailableDays=AvailableDays,
                AvailableTime=AvailableTime,
                SlotDurationMinutes=SlotDurationMinutes,
                About=About,
                Reviews=Reviews,
                Status=Status,
                ProfilePhotoUrl=img_path
            )
            return await self.manager.create_doctor(obj)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_doctors(self):
        return await self.manager.get_doctors()

    async def get_doctor_by_id(self, doctor_id: int):
        doctor = await self.manager.get_doctor_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor

    async def update_doctor(
        self,
        doctor_id: int,
        FirstName: str = Form(None),
        LastName: str = Form(None),
        Gender: str = Form(None),
        DateOfBirth: str = Form(None),
        Email: str = Form(None),
        MobileNumber: str = Form(None),
        Specialization: str = Form(None),
        Qualifications: str = Form(None),
        ExperienceYears: int = Form(None),
        LicenseNumber: str = Form(None),
        ClinicName: str = Form(None),
        ClinicAddress: str = Form(None),
        City: str = Form(None),
        State: str = Form(None),
        Country: str = Form(None),
        PostalCode: str = Form(None),
        ConsultationFee: float = Form(None),
        AvailableDays: str = Form(None),
        AvailableTime: str = Form(None),
        SlotDurationMinutes: int = Form(None),
        About: str = Form(None),
        Reviews: str = Form(None),
        Status: str = Form(None),
        ProfilePhoto: UploadFile = File(None)
    ):
        try:
            old_data = await self.manager.get_doctor_by_id(doctor_id)
            if not old_data:
                raise HTTPException(status_code=404, detail="Doctor not found")

            update_data = {}
            for field_name, value in {
                "FirstName": FirstName,
                "LastName": LastName,
                "Gender": Gender,
                "DateOfBirth": DateOfBirth,
                "Email": Email,
                "MobileNumber": MobileNumber,
                "Specialization": Specialization,
                "Qualifications": Qualifications,
                "ExperienceYears": ExperienceYears,
                "LicenseNumber": LicenseNumber,
                "ClinicName": ClinicName,
                "ClinicAddress": ClinicAddress,
                "City": City,
                "State": State,
                "Country": Country,
                "PostalCode": PostalCode,
                "ConsultationFee": ConsultationFee,
                "AvailableDays": AvailableDays,
                "AvailableTime": AvailableTime,
                "SlotDurationMinutes": SlotDurationMinutes,
                "About": About,
                "Reviews": Reviews,
                "Status": Status
            }.items():
                if value is not None:
                    update_data[field_name] = value

            if ProfilePhoto:
                new_path = await save_picture(ProfilePhoto, "Doctor")
                old_path = old_data.ProfilePhotoUrl
                if old_path:
                    abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_path))
                    if os.path.exists(abs_old_path):
                        os.remove(abs_old_path)
                update_data["ProfilePhotoUrl"] = new_path

            return await self.manager.update_doctor(doctor_id, DoctorUpdate(**update_data))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_doctor(self, doctor_id: int):
        try:
            old_data = await self.manager.get_doctor_by_id(doctor_id)
            if old_data and old_data.ProfilePhotoUrl:
                abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_data.ProfilePhotoUrl))
                if os.path.exists(abs_old_path):
                    os.remove(abs_old_path)
            return await self.manager.delete_doctor(doctor_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))



# --------------------------------------------------
# Doctor Appointment API
# --------------------------------------------------
class DoctorAppointmentAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = DoctorAppointmentManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/doctor-appointments")(self.create_appointment)
        self.router.get("/doctor-appointments/{appointment_id}")(self.get_appointment_by_id)
        self.router.get("/doctor-appointments/doctor/{doctor_id}")(self.get_appointments_by_doctor)
        self.router.put("/doctor-appointments/{appointment_id}")(self.update_appointment)
        self.router.delete("/doctor-appointments/{appointment_id}")(self.delete_appointment)

    async def create_appointment(self, data: DoctorAppointmentCreate):
        return await self.manager.create_appointment(data)

    async def get_appointment_by_id(self, appointment_id: int):
        return await self.manager.get_appointment_by_id(appointment_id)

    async def get_appointments_by_doctor(self, doctor_id: int):
        return await self.manager.get_appointments_by_doctor(doctor_id)

    async def update_appointment(self, appointment_id: int, data: DoctorAppointmentUpdate):
        return await self.manager.update_appointment(appointment_id, data)

    async def delete_appointment(self, appointment_id: int):
        return await self.manager.delete_appointment(appointment_id)
