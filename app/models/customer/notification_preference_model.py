from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .sql_base import Base


# -------------------------------------------------
# Notification Preference Model
# -------------------------------------------------
class NotificationPreference(Base):
    __tablename__ = "NotificationPreference"

    PreferenceId = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key to Customer
    CustomerId = Column(Integer, ForeignKey("customer.CustomerId"), nullable=False, unique=True)
    
    # Notification Settings
    EnableWhatsApp = Column(Boolean, default=True)
    EnableSMS = Column(Boolean, default=True)
    EnableEmail = Column(Boolean, default=False)
    EnablePushNotification = Column(Boolean, default=True)
    
    # Default Preference
    DefaultChannel = Column(String(20), default="both")  # whatsapp, sms, email, push, both
    
    # Service Request Notifications
    NotifyOnRequestCreated = Column(Boolean, default=True)
    NotifyOnProviderAssigned = Column(Boolean, default=True)
    NotifyOnRequestAccepted = Column(Boolean, default=True)
    NotifyOnRequestCompleted = Column(Boolean, default=True)
    NotifyOnRequestCancelled = Column(Boolean, default=True)
    
    # Promotional Notifications
    NotifyOnPromotions = Column(Boolean, default=False)
    NotifyOnNewServices = Column(Boolean, default=False)
    
    # Quiet Hours
    QuietHoursStart = Column(String(5), nullable=True)  # Format: "HH:MM"
    QuietHoursEnd = Column(String(5), nullable=True)   # Format: "HH:MM"
    EnableQuietHours = Column(Boolean, default=False)
