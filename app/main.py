from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# Customer
from app.api.customer.customer_api import CustomerAPI
from app.api.customer.customer_dashboard_api import CustomerDashboardAPI
from app.api.customer.medicine_api import MedicineAPI, MedicineCategoryAPI, MedicineInfoAPI, MedicalTypeAPI
from app.api.customer.cart_api import CartAPI
from app.api.customer.order_api import OrderAPI, OrderItemAPI
from app.api.customer.prescription_api import PrescriptionAPI
from app.api.customer.customer_notification_api import CustomerNotificationAPI
from app.api.customer.lap_api import LabAPI, TestAPI, AppointmentAPI
from app.api.customer.doctor_api import DoctorAPI, DoctorAppointmentAPI
from app.api.customer.retailer_api import RetailerAPI
from app.api.customer.service_provider_api import ServiceProviderAPI
from app.api.customer.service_list_api import ServiceListAPI
from app.api.customer.provider_services_api import ProviderServicesAPI
from app.api.customer.service_provider_dashboard_api import ServiceProviderDashboardAPI
from app.api.customer.service_request_api import ServiceRequestAPI


app = FastAPI(title="Medical App API list")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow all origins
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods
    allow_headers=["*"],          # allow all headers
)

app.mount("/Images", StaticFiles(directory="Images"), name="Images")


# Customer
customer_api = CustomerAPI()
customer_dashboard_api = CustomerDashboardAPI()
customer_notification_api = CustomerNotificationAPI()
medical_type_api = MedicalTypeAPI()
medicine_category_api = MedicineCategoryAPI()
medicine_api = MedicineAPI()
medicine_info_api = MedicineInfoAPI()
cart = CartAPI()
order_api = OrderAPI()
order_item_api = OrderItemAPI()
prescription = PrescriptionAPI()
lab_api = LabAPI()
test_api = TestAPI()
appointment_api = AppointmentAPI()
doctor_api = DoctorAPI()
doctor_appointment_api = DoctorAppointmentAPI()
retailer_api = RetailerAPI()
service_provider_api = ServiceProviderAPI()
service_list_api = ServiceListAPI()
provider_services_api = ProviderServicesAPI()
service_provider_dashboard_api = ServiceProviderDashboardAPI()
service_request_api = ServiceRequestAPI()



# Customer
app.include_router(medicine_api.router, tags=["Medicine"])
app.include_router(medical_type_api.router, tags=["Medical Type"])
# app.include_router(medicine_info_api.router, tags=["Medicine Info"])
app.include_router(medicine_category_api.router, tags=["Medicine Category"])
app.include_router(cart.router, tags=["Cart"])
app.include_router(order_api.router, tags=["Orders"])
app.include_router(order_item_api.router, tags=["Order Items"])
app.include_router(prescription.router, tags=["Prescription"])
app.include_router(customer_api.router, tags=["Customer"])
app.include_router(customer_dashboard_api.router, tags=["Customer Dashboard"])
app.include_router(customer_notification_api.router, tags=["Customer Notifications"])
app.include_router(lab_api.router, tags=["Lap"])
# app.include_router(test_api.router, tags=["Test"])
# app.include_router(appointment_api.router, tags=["Appoinment"])
app.include_router(doctor_api.router, tags=["Doctor"])
# app.include_router(doctor_appointment_api.router, tags=["Doctor Appoinment"])
app.include_router(retailer_api.router, tags=["Retailer"])
app.include_router(service_provider_api.router, tags=["Service Provider"])
app.include_router(service_list_api.router, tags=["Service List"])
app.include_router(provider_services_api.router, tags=["Provider Services"])
app.include_router(service_provider_dashboard_api.router, tags=["Service Provider Dashboard"])
app.include_router(service_request_api.router, tags=["Service Request"])





