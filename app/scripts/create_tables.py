import sqlite3
from sqlite3 import Connection

class TableCreator:
    def __init__(self, sqlite_url: str):
        # Parse file path from SQLAlchemy-style URL
        if sqlite_url.startswith("sqlite+aiosqlite:///"):
            self.db_file = sqlite_url.replace("sqlite+aiosqlite:///", "")
        else:
            raise ValueError("Invalid SQLite URL format")

    def get_connection(self) -> Connection:
        return sqlite3.connect(self.db_file)
    

    # ------------------------
    # Customer Table
    # ------------------------
    
    def create_customer_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Customer (
            CustomerId INTEGER PRIMARY KEY AUTOINCREMENT,
            FullName TEXT,
            ProfilePicture TEXT,
            DateOfBirth DATE,
            Gender TEXT,
            Email TEXT NOT NULL UNIQUE,
            PasswordHash TEXT NOT NULL,
            PhoneNumber TEXT,

            AddressLine1 TEXT NOT NULL,
            AddressLine2 TEXT,
            City TEXT NOT NULL,
            State TEXT NOT NULL,
            Country TEXT NOT NULL,
            PostalCode TEXT NOT NULL,
            Latitude REAL,
            Longitude REAL,

            BankName TEXT,
            AccountNumber TEXT,
            IFSCCode TEXT,
            Branch TEXT
        );
        """
        self._execute(sql, "Customer")




    # ------------------------
    # 1. MedicalType Table
    # ------------------------
    def create_medicine_type_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS MedicalType (
            MedicalTypeId INTEGER PRIMARY KEY AUTOINCREMENT,
            MedicalType TEXT NOT NULL,
            ImgUrl TEXT
        );
        """
        self._execute(sql, "MedicalType")

    # ------------------------
    # 2. MedicineCategory Table
    # ------------------------
    def create_medicine_category_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS MedicineCategory (
            MedicineCategoryId INTEGER PRIMARY KEY AUTOINCREMENT,
            MedicalTypeId INTEGER NOT NULL,
            Category TEXT NOT NULL,
            ImgUrl TEXT
        );
        """
        self._execute(sql, "MedicineCategory")

    # ------------------------
    # 3. Medicine Table
    # ------------------------
    def create_medicine_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Medicine (
            MedicineId INTEGER PRIMARY KEY AUTOINCREMENT,
            MedicalTypeId INTEGER,
            MedicineCategoryId INTEGER,
            Name TEXT NOT NULL,
            GenericName TEXT,
            DosageForm TEXT,
            Strength TEXT,
            Manufacturer TEXT,
            PrescriptionRequired BOOLEAN DEFAULT 0,
            Size TEXT,
            UnitPrice REAL NOT NULL,
            TherapeuticClass TEXT,
            ImgUrl TEXT            
        );
        """
        self._execute(sql, "Medicine")


    # ------------------------
    # 4. MedicineInfo Table
    # ------------------------
    def create_medicine_info_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS MedicineInfo (
            MedicineInfoId INTEGER PRIMARY KEY AUTOINCREMENT,
            MedicineId INTEGER NOT NULL,
            QuickFacts TEXT,
            AlternateMedicines TEXT,
            SideEffects TEXT,
            HowWorks TEXT,
            Notes TEXT,
            Uses TEXT,
            Precautions TEXT,
            GeneralGuide TEXT
        );
        """
        self._execute(sql, "MedicineInfo")


    # ------------------------------------------------------------------
    # 2️⃣ CustomerNotification
    # ------------------------------------------------------------------
    def create_customer_notification_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS CustomerNotification (
            NotificationId INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerId INTEGER NOT NULL,
            Title TEXT NOT NULL,
            Message TEXT NOT NULL,
            Type TEXT NOT NULL,
            IsRead BOOLEAN DEFAULT 0,
            Date DATETIME DEFAULT CURRENT_TIMESTAMP,
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self._execute(sql, "CustomerNotification")


    def create_cart_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Cart (
            CartId INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerId INTEGER NOT NULL,
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self._execute(sql, "Cart")

    def create_cart_item_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS CartItem (
            CartItemId INTEGER PRIMARY KEY AUTOINCREMENT,
            CartId INTEGER NOT NULL,
            MedicineId INTEGER NOT NULL,
            Quantity INTEGER NOT NULL,
            StoredPrice REAL NOT NULL
        );
        """
        self._execute(sql, "CartItem")


    def create_order_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Orders (
            OrderId INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerId INTEGER NOT NULL,
            RetailerId INTEGER NOT NULL,
            OrderDateTime DATETIME DEFAULT CURRENT_TIMESTAMP,
            ExpectedDelivery DATETIME,
            
            -- Delivery info
            DeliveryMode TEXT,
            DeliveryService TEXT,
            DeliveryPartnerTrackingId TEXT,
            DeliveryStatus TEXT DEFAULT 'Pending',
            
            -- Payment info
            PaymentMode TEXT,
            PaymentStatus TEXT DEFAULT 'Pending',
            Amount REAL DEFAULT 0,  -- total including GST
            
            -- Prescription info
            PrescriptionFileUrl TEXT,
            PrescriptionVerified BOOLEAN DEFAULT 0,
            
            -- Order state
            OrderStatus TEXT DEFAULT 'New',
            
            -- Audit fields
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self._execute(sql, "Orders")


    def create_order_item_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS OrderItem (
            OrderItemId INTEGER PRIMARY KEY AUTOINCREMENT,
            OrderId INTEGER NOT NULL,
            CustomerId INTEGER NOT NULL,
            RetailerId INTEGER NOT NULL,
            MedicineId INTEGER NOT NULL,
            Quantity INTEGER NOT NULL,
            GSTPercentage REAL NOT NULL,
            TotalAmount REAL NOT NULL
        );
        """
        self._execute(sql, "OrderItem")




    # ------------------------------------------------------------------
    # 6️⃣ Prescriptions
    # ------------------------------------------------------------------
    def create_prescription_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Prescription (
            PrescriptionId INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerId INTEGER NOT NULL,
            OrderId INTEGER NOT NULL,
            DoctorName TEXT,
            DocumentUrl TEXT NOT NULL,
            Status TEXT NOT NULL,
            Verified BOOLEAN DEFAULT 0,
            VerifiedBy TEXT,
            UploadedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self._execute(sql, "Prescription")

    
    def create_lab_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Lab (
            LabId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Contact TEXT,
            Email TEXT,
            Timings TEXT,
            Reviews TEXT,
            
            AddressLine1 TEXT,
            AddressLine2 TEXT,
            City TEXT,
            State TEXT,
            Country TEXT,
            PostalCode TEXT,
            Latitude TEXT,
            Longitude TEXT,
            ShopPic TEXT,

            CreatedAt TEXT,
            UpdatedAt TEXT
        );
        """
        self._execute(sql, "Lab")

    
    def create_test_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Test (
            TestId INTEGER PRIMARY KEY AUTOINCREMENT,
            LabId INTEGER NOT NULL,
            Name TEXT NOT NULL,
            Preparation TEXT,
            Price REAL NOT NULL,
            GstPercent REAL,
            Category TEXT,
            EstimatedReportTime TEXT,

            CreatedAt TEXT,
            UpdatedAt TEXT
        );
        """
        self._execute(sql, "Test")


    def create_appointment_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Appointment (
            AppointmentId INTEGER PRIMARY KEY AUTOINCREMENT,
            AppointmentNo TEXT,

            LabId INTEGER NOT NULL,
            PatientName TEXT,
            PatientAge INTEGER,
            PatientGender TEXT,
            ContactNumber TEXT,
            Email TEXT,
            Address TEXT,
            GPSLocation TEXT,

            AppointmentDate TEXT,
            TimeSlot TEXT,
            SelectedTests TEXT,

            SampleCollectionMode TEXT,
            TotalAmount REAL,
            TotalGst REAL,
            NetPayable REAL,
            PaymentMethod TEXT,
            PaymentStatus TEXT,
            BookingStatus TEXT,

            CreatedAt TEXT,
            UpdatedAt TEXT
        );
        """
        self._execute(sql, "Appointment")

    def create_doctor_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Doctor (
            DoctorId INTEGER PRIMARY KEY AUTOINCREMENT,
            
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Gender TEXT,
            DateOfBirth TEXT,
            Email TEXT,
            MobileNumber TEXT,

            Specialization TEXT,
            Qualifications TEXT,
            ExperienceYears INTEGER,
            LicenseNumber TEXT,

            ClinicName TEXT,
            ClinicAddress TEXT,
            City TEXT,
            State TEXT,
            Country TEXT,
            PostalCode TEXT,

            ConsultationFee REAL,
            AvailableDays TEXT,
            AvailableTime TEXT,
            SlotDurationMinutes INTEGER,

            ProfilePhotoUrl TEXT,
            About TEXT,
            Reviews TEXT,
            Status TEXT,

            CreatedAt TEXT,
            UpdatedAt TEXT
        );
        """
        self._execute(sql, "Doctor")

    def create_doctor_appointment_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS DoctorAppointment (
            AppointmentId INTEGER PRIMARY KEY AUTOINCREMENT,
            DoctorId INTEGER NOT NULL,

            PatientName TEXT,
            MobileNumber TEXT,
            Age INTEGER,
            Gender TEXT,

            AppointmentMode TEXT,
            AppointmentDate TEXT,
            AppointmentSlot TEXT,
            AppointmentTime TEXT,

            Status TEXT,
            PaymentStatus TEXT,
            PaymentMethod TEXT,

            ReasonForVisit TEXT,
            Notes TEXT,

            CreatedAt TEXT,
            UpdatedAt TEXT,

            FOREIGN KEY (DoctorId) REFERENCES Doctor(DoctorId)
        );
        """
        self._execute(sql, "DoctorAppointment")



    # Retailer Tables
    # ------------------------------------------------------------------
    # 1️⃣ Retailer
    # ------------------------------------------------------------------
    def create_retailer_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Retailer (
            RetailerId INTEGER PRIMARY KEY AUTOINCREMENT,
            ShopName TEXT,
            OwnerName TEXT,
            GSTNumber TEXT,
            LicenseNumber TEXT,
            PhoneNumber TEXT,
            Email TEXT,
            PasswordHash TEXT,
            AddressLine1 TEXT NOT NULL,
            AddressLine2 TEXT,
            City TEXT NOT NULL,
            State TEXT NOT NULL,
            Country TEXT NOT NULL,
            PostalCode TEXT NOT NULL,
            Latitude REAL,
            Longitude REAL,
            ShopPic TEXT,
            BankName TEXT,
            AccountNumber TEXT,
            IFSCCode TEXT,
            Branch TEXT
        );
        """
        self._execute(sql, "Retailer")




    def add_column_if_not_exists(self, table: str, column: str, datatype: str):
        """
        Safely adds a new column to a table only if it does not already exist.
        Works for SQLite.
        """
        try:
            # 1. Get existing table schema
            schema_query = f"PRAGMA table_info({table});"
            columns = self._fetchall(schema_query)

            # 2. Check if column already exists
            existing_columns = [col[1] for col in columns]  # col[1] = column name

            if column in existing_columns:
                print(f"Column '{column}' already exists in table '{table}'. Skipping.")
                return

            # 3. Add new column
            alter_sql = f"ALTER TABLE {table} ADD COLUMN {column} {datatype};"
            self._execute(alter_sql, f"Add column {column}")

            print(f"Column '{column}' added successfully to '{table}'.")
        
        except Exception as e:
            print(f"Error adding column '{column}' to '{table}': {e}")

    def _fetchall(self, sql: str):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return []
        finally:
            conn.close()

    def remove_column_if_exists(self, table: str, column: str):
        """
        Removes a column from a SQLite table by rebuilding the table.
        Simplified version: copies all columns except the one to remove.
        """
        try:
            # 1. Get existing columns
            columns = [c[1] for c in self._fetchall(f"PRAGMA table_info({table});")]

            if column not in columns:
                print(f"Column '{column}' does not exist in '{table}'. Skipping.")
                return

            # Columns to keep
            keep_cols = [c for c in columns if c != column]
            cols_str = ", ".join(keep_cols)

            conn = self.get_connection()
            cur = conn.cursor()

            # 2. Read original CREATE TABLE statement
            cur.execute(f"""
                SELECT sql FROM sqlite_master
                WHERE type='table' AND name='{table}';
            """)
            create_sql = cur.fetchone()[0]

            # 3. Build new CREATE TABLE without the column definition
            inside = create_sql[create_sql.index("(")+1 : create_sql.rindex(")")]
            new_inside = ", ".join(
                part.strip()
                for part in inside.split(",")
                if not part.strip().startswith(column + " ")
            )
            new_create_sql = f"CREATE TABLE {table}_new ({new_inside});"

            # 4. Rebuild table
            cur.execute(new_create_sql)
            cur.execute(f"INSERT INTO {table}_new ({cols_str}) SELECT {cols_str} FROM {table};")
            cur.execute(f"DROP TABLE {table};")
            cur.execute(f"ALTER TABLE {table}_new RENAME TO {table};")

            conn.commit()

            print(f"Column '{column}' removed successfully from '{table}'.")

        except Exception as e:
            print(f"❌ Error removing column '{column}': {e}")

        finally:
            try:
                conn.close()
            except:
                pass

    def remove_table_if_exists(self, table: str):
        """
        Removes a table from the SQLite database if it exists.
        """
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()

            # Check if table exists
            cur.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name=?;
            """, (table,))
            
            if not cur.fetchone():
                print(f"Table '{table}' does not exist. Skipping.")
                return

            # Drop table
            cur.execute(f"DROP TABLE {table};")
            conn.commit()

            print(f"Table '{table}' removed successfully.")

        except Exception as e:
            print(f"❌ Error removing table '{table}': {e}")

        finally:
            try:
                if conn:
                    conn.close()
            except:
                pass



    # ------------------------------------------------------------------
    # INTERNAL HELPER
    # ------------------------------------------------------------------
    def _execute(self, sql: str, table_name: str):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            print(f"✅ Table '{table_name}' created successfully!")
        except Exception as e:
            print(f"❌ Error creating table '{table_name}':", e)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # MAIN CREATION FUNCTION
    # ------------------------------------------------------------------
    def create_all_tables(self):
        # Customer tables
        self.create_customer_table()
        self.create_medicine_type_table()
        self.create_medicine_category_table()
        self.create_medicine_table()
        # self.create_medicine_info_table()


        # self.create_customer_notification_table()
        self.create_cart_table()
        self.create_cart_item_table()
        self.create_prescription_table()

        self.create_order_table()
        self.create_order_item_table()
                
        # self.create_lab_table()
        # self.create_test_table()
        # self.create_appointment_table()

        # self.create_doctor_table()
        # self.create_doctor_appointment_table()

        self.create_retailer_table()


        # self.add_column_if_not_exists("RetailerOrders", "RetailerName", "TEXT")
        # self.remove_column_if_exists("RetailerOrders", "DistributorrName")
        # self.remove_table_if_exists("Medicine")


        # tables = [
        #     "MedicalType", "MedicineCategory", "Medicine", "Customer", "Address", "Retailer",
        #     "Orders", "OrderItem", "RetailerNotification", "CustomerInvoice", "CustomerInvoiceItem",
        #     "RetailerOrders", "RetailerOrderItem", "Prescription", "CustomerNotification",
        #     "DistributorNotification", "RetailerInvoice", "RetailerInvoiceItem", "Lab",
        #     "Doctor", "MedicalFacility", "MedicalLab"
        # ]

        # for table in tables:
        #     self.remove_table_if_exists(table)





if __name__ == "__main__":
    sqlite_url = "sqlite+aiosqlite:///./medical.db"
    creator = TableCreator(sqlite_url)
    creator.create_all_tables()

