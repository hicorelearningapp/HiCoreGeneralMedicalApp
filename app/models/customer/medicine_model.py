from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.dialects.sqlite import JSON
from .sql_base import Base

# ------------------------------------------------
# Medicine Type
# ------------------------------------------------
class MedicalType(Base):
    __tablename__ = "MedicalType"

    MedicalTypeId = Column(Integer, primary_key=True, index=True)
    MedicalType = Column(String, nullable=False)
    ImgUrl = Column(String, nullable=True)


# ------------------------------------------------
# Medicine Category
# ------------------------------------------------
class MedicineCategory(Base):
    __tablename__ = "MedicineCategory"

    MedicineCategoryId = Column(Integer, primary_key=True, index=True)
    MedicalTypeId = Column(Integer, nullable=False)
    Category = Column(String, nullable=False)
    ImgUrl = Column(String, nullable=True)


# ------------------------------------------------
# Medicine Model
# ------------------------------------------------
class Medicine(Base):
    __tablename__ = "Medicine"

    MedicineId = Column(Integer, primary_key=True, index=True)
    MedicalTypeId = Column(Integer, nullable=True)
    MedicineCategoryId = Column(Integer, nullable=True)
    Name = Column(String, nullable=False)
    GenericName = Column(String, nullable=True)
    DosageForm = Column(String, nullable=True)
    Strength = Column(String, nullable=True)
    Manufacturer = Column(String, nullable=True)

    PrescriptionRequired = Column(Boolean, default=False)
    Size = Column(Integer, nullable=True)
    UnitPrice = Column(Float, nullable=False)
    TherapeuticClass = Column(String, nullable=True)
    ImgUrl = Column(String, nullable=True)

    



# ------------------------------------------------
# Medicine Info
# ------------------------------------------------
class MedicineInfo(Base):
    __tablename__ = "MedicineInfo"

    MedicineInfoId = Column(Integer, primary_key=True, index=True)
    MedicineId = Column(Integer, nullable=False)

    QuickFacts = Column(String, nullable=True)
    AlternateMedicines = Column(String, nullable=True)
    SideEffects = Column(String, nullable=True)
    HowWorks = Column(String, nullable=True)
    Notes = Column(String, nullable=True)
    Uses = Column(String, nullable=True)
    Precautions = Column(String, nullable=True)
    GeneralGuide = Column(String, nullable=True)
