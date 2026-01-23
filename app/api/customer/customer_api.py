import os
from fastapi import APIRouter, HTTPException

from ...config import settings
from ...schemas.customer.customer_schema import (
    CustomerCreate,
    CustomerUpdate,
    CustomerRead
)
from ...crud.customer.customer_manager import CustomerManager
from ...utils.image_uploader import save_picture
from fastapi import Form, File, UploadFile


class CustomerAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = CustomerManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/customers", response_model=dict)(self.create_customer)
        self.router.get("/customers/{customer_id}", response_model=dict)(self.get_customer)
        self.router.get("/customers", response_model=dict)(self.get_all_customers)
        self.router.put("/customers/{customer_id}", response_model=dict)(self.update_customer)
        self.router.delete("/customers/{customer_id}", response_model=dict)(self.delete_customer)

    # async def create_customer(self, customer: CustomerCreate):
    #     try:
    #         return await self.crud.create_customer(customer)
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))


    async def create_customer(
        self,
        FullName: str = Form(None),
        Email: str = Form(...),
        Password: str = Form(...),
        PhoneNumber: str = Form(None),
        ProfilePicture: UploadFile = File(None),
        DateOfBirth: str = Form(None),
        Gender: str = Form(None),
        AddressLine1: str = Form(...),
        AddressLine2: str = Form(None),
        City: str = Form(...),
        State: str = Form(...),
        Country: str = Form(...),
        PostalCode: str = Form(...),
        Latitude: float = Form(None),
        Longitude: float = Form(None),
        BankName: str = Form(None),
        AccountNumber: str = Form(None),
        IFSCCode: str = Form(None),
        Branch: str = Form(None)
    ):
        try:
            # save image
            profile_path = await save_picture(ProfilePicture, "Profile")

            # Build CustomerCreate Pydantic object
            customer_obj = CustomerCreate(
                FullName=FullName,
                Email=Email,
                Password=Password,
                PhoneNumber=PhoneNumber,
                ProfilePicture=profile_path,
                DateOfBirth=DateOfBirth,
                Gender=Gender,
                AddressLine1=AddressLine1,
                AddressLine2=AddressLine2,
                City=City,
                State=State,
                Country=Country,
                PostalCode=PostalCode,
                Latitude=Latitude,
                Longitude=Longitude,
                BankName=BankName,
                AccountNumber=AccountNumber,
                IFSCCode=IFSCCode,
                Branch=Branch,
            )

            return await self.crud.create_customer(customer_obj)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_customer(self, customer_id: int):
        try:
            return await self.crud.get_customer(customer_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_customers(self):
        try:
            return await self.crud.get_all_customers()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_customer(
        self,
        customer_id: int,
        FullName: str = Form(None),
        Email: str = Form(None),
        Password: str = Form(None),
        PhoneNumber: str = Form(None),
        DateOfBirth: str = Form(None),
        Gender: str = Form(None),
        AddressLine1: str = Form(...),
        AddressLine2: str = Form(None),
        City: str = Form(...),
        State: str = Form(...),
        Country: str = Form(...),
        PostalCode: str = Form(...),
        Latitude: float = Form(None),
        Longitude: float = Form(None),
        BankName: str = Form(None),
        AccountNumber: str = Form(None),
        IFSCCode: str = Form(None),
        Branch: str = Form(None),
        ProfilePicture: UploadFile = File(None),
    ):
        try:
            # Fetch current customer first (to delete old image if replaced)
            old_customer = await self.crud.get_customer(customer_id)
            if not old_customer["success"]:
                raise HTTPException(status_code=404, detail="Customer not found")

            update_data = {}

            # Update text fields if provided
            for field_name, value in {
                "FullName": FullName,
                "Email": Email,
                "Password": Password,
                "PhoneNumber": PhoneNumber,
                "DateOfBirth": DateOfBirth,
                "Gender": Gender,
                "AddressLine1": AddressLine1,
                "AddressLine2": AddressLine2,
                "City": City,
                "State": State,
                "Country": Country,
                "PostalCode": PostalCode,
                "Latitude": Latitude,
                "Longitude": Longitude,
                "BankName": BankName,
                "AccountNumber": AccountNumber,
                "IFSCCode": IFSCCode,
                "Branch": Branch,
            }.items():
                if value is not None:
                    # Rename Password to PasswordHash for DB
                    if field_name == "Password":
                        update_data["PasswordHash"] = value
                    else:
                        update_data[field_name] = value

            # Handle profile picture
            if ProfilePicture:
                new_path = await save_picture(ProfilePicture, "Profile")

                # Delete old image safely
                old_path = old_customer["data"]["ProfilePicture"]
                if old_path:
                    abs_old_path = os.path.normpath(os.path.join(os.getcwd(), old_path))
                    if os.path.exists(abs_old_path):
                        os.remove(abs_old_path)
                        print(f"Deleted old profile image: {abs_old_path}")
                    else:
                        print(f"Old profile image does not exist: {abs_old_path}")

                update_data["ProfilePicture"] = new_path

            # Update DB using your CRUD
            return await self.crud.update_customer(customer_id, CustomerUpdate(**update_data))

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    
    async def delete_customer(self, customer_id: int):
        try:
            customer = await self.crud.get_customer(customer_id)
            if not customer["success"]:
                raise HTTPException(status_code=404, detail="Customer not found")

            image_path = customer["data"]["ProfilePicture"]

            # delete customer from DB
            result = await self.crud.delete_customer(customer_id)

            # Delete physical file
            if image_path:
                # Convert to absolute path
                BASE_DIR = os.getcwd()   # your project root directory
                abs_path = os.path.join(BASE_DIR, image_path)
                abs_path = os.path.normpath(abs_path) 

                print("Deleting:", abs_path)  # debugging

                if os.path.exists(abs_path):
                    os.remove(abs_path)
                else:
                    print("File does not exist:", abs_path)

            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))



