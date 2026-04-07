"""
Script to insert sample data into Customer, ServiceProvider, and ServiceRequest tables.
"""
import sqlite3
from datetime import datetime

def insert_sample_data():
    db_file = "medical.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Check if sample data already exists
    cursor.execute("SELECT COUNT(*) FROM ServiceProvider WHERE ProviderName LIKE 'service provider%'")
    provider_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM customer WHERE CustomerName LIKE 'customer%'")
    customer_count = cursor.fetchone()[0]
    
    if provider_count > 0 or customer_count > 0:
        print("Sample data already exists. Skipping insertion.")
        conn.close()
        return
    
    # Insert 2 Customers
    sample_customers = [
        (
            "customer1", None, "1990-01-01", "Male", "customer1@test.com", None, "9876543210",
            "123 Main St, City", "Apt 4B", "New York", "NY", "10001",
            40.7128, -74.0060, "Bank of America", "1234567890", "BOFA0123", "Main Branch"
        ),
        (
            "customer2", None, "1985-05-15", "Female", "customer2@test.com", None, "9876543211",
            "456 Oak Ave, Town", None, "Los Angeles", "CA", "90001",
            34.0522, -118.2437, "Chase Bank", "0987654321", "CHAS0456", "Downtown Branch"
        )
    ]
    
    cursor.executemany("""
        INSERT INTO customer (
            CustomerName, ProfilePicture, DateOfBirth, Gender, Email, PasswordHash, CustomerPhoneNumber,
            AddressLine1, AddressLine2, City, State, PostalCode,
            Latitude, Longitude, BankName, AccountNumber, IFSCCode, Branch
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_customers)
    
    print(f"Inserted {len(sample_customers)} customers")
    
    # Insert 2 Service Providers
    sample_providers = [
        (
            "service provider 1", None, None, None,
            "123 Main St, City", "10001",
            "9876543201", "provider1@test.com", "password1", 5, "Male", "1990-01-01",
            "LIC001", "available", 4.5, 1, 1, "General Care", 
            "General medical assistance", '["Medical Assistant", "Nursing Care"]'
        ),
        (
            "service provider 2", None, None, None,
            "456 Oak St, Town", "90001",
            "9876543202", "provider2@test.com", "password2", 3, "Female", "1992-05-15",
            "LIC002", "available", 4.0, 1, 1, "Nursing",
            "Professional nursing care", '["Nursing Care", "Elder Care"]'
        )
    ]
    
    cursor.executemany("""
        INSERT INTO ServiceProvider (
            ProviderName, PhotoUrl, CertificateUrl, AadhaarOrIdProofUrl,
            Address, Pincode, PhoneNumber, Email, Password, ExperienceYears,
            Gender, DateOfBirth, LicenseNumber, AvailabilityStatus, Rating, IsVerified, IsActive,
            Specialization, ServiceDescription, ServicesOffered
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_providers)
    
    print(f"Inserted {len(sample_providers)} service providers")
    
    # Get the inserted provider and customer IDs
    cursor.execute("SELECT ServiceProviderId, ProviderName FROM ServiceProvider WHERE ProviderName LIKE 'service provider%'")
    providers = {name: id for id, name in cursor.fetchall()}
    cursor.execute("SELECT CustomerId, CustomerName FROM customer WHERE CustomerName LIKE 'customer%'")
    customers = {name: id for id, name in cursor.fetchall()}
    
    print(f"Provider IDs: {providers}")
    print(f"Customer IDs: {customers}")
    
    # Insert 3 Service Requests

    sample_requests = [
        (
            customers.get("customer1"),
            providers.get("service provider 1"),
            "General Checkup",
            "customer1",
            "9876543210",
            "123 Customer St, City",
            "2024-04-10",
            "10:00 AM",
            "General checkup needed",
            "560001",
            "pending",
            None, None, None, None,
            "Customer needs regular checkup",
            None,
            500.0,
            None,
            "pending",
            "random",
            "both"
        ),
        (
            customers.get("customer1"),
            providers.get("service provider 2"),
            "Post Surgery Care",
            "customer1",
            "9876543210",
            "456 Customer Ave, Town",
            "2024-04-11",
            "2:00 PM",
            "Post-surgery care required",
            "560002",
            "assigned",
            datetime.now().isoformat(),
            None, None, None,
            None,
            "Provider assigned for post-op care",
            800.0,
            None,
            "pending",
            "manual",
            "both"
        ),
        (
            customers.get("customer2"),
            providers.get("service provider 1"),
            "Rehabilitation Therapy",
            "customer2",
            "9876543211",
            "789 Customer Rd, Village",
            "2024-04-12",
            "11:00 AM",
            "Rehabilitation therapy needed",
            "560003",
            "accepted",
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            None, None,
            "Sports injury rehabilitation",
            "Provider confirmed availability",
            1200.0,
            None,
            "pending",
            "random",
            "whatsapp"
        )
    ]

    cursor.executemany("""
        INSERT INTO ServiceRequest (
            CustomerId, ServiceProviderId, ServiceName, CustomerName, CustomerPhone,
            CustomerAddress, PreferredDate, PreferredTime, RequestDescription,
            Pincode, Status, AssignedAt, AcceptedAt, CompletedAt, CancelledAt,
            CustomerNotes, ProviderNotes, EstimatedPrice, FinalPrice,
            PaymentStatus, AssignmentMode, NotificationPreference
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_requests)
    
    print(f"Inserted {len(sample_requests)} service requests")
    
    # Insert Notification Preferences for customers
    notification_preferences = [
        (customers.get("customer1"), 1, 1, 0, 1, "both", 1, 1, 1, 1, 1, 0, 0, "22:00", "08:00", 1),
        (customers.get("customer2"), 1, 0, 1, 1, "sms", 1, 1, 1, 1, 1, 1, 0, None, None, 0)
    ]
    
    cursor.executemany("""
        INSERT INTO NotificationPreference (
            CustomerId, EnableWhatsApp, EnableSMS, EnableEmail, EnablePushNotification,
            DefaultChannel, NotifyOnRequestCreated, NotifyOnProviderAssigned, NotifyOnRequestAccepted,
            NotifyOnRequestCompleted, NotifyOnRequestCancelled, NotifyOnPromotions, NotifyOnNewServices,
            QuietHoursStart, QuietHoursEnd, EnableQuietHours
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, notification_preferences)
    
    print(f"Inserted {len(notification_preferences)} notification preferences")
    
    conn.commit()
    conn.close()
    print("✅ Sample data inserted successfully!")

if __name__ == "__main__":
    insert_sample_data()
