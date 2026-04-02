"""
Notification Service Utility
============================
Placeholder implementation for SMS and WhatsApp notifications.
This module provides a reusable interface for sending notifications.
Actual provider integration (Twilio, WhatsApp Business API, etc.) to be added later.
"""

from typing import Optional, Literal
from .logger import get_logger

logger = get_logger(__name__)


# ------------------------------------------------------------
# Notification Service
# ------------------------------------------------------------
class NotificationService:
    """
    Service for sending SMS and WhatsApp notifications to customers.
    Currently uses placeholder methods - actual provider integration pending.
    """

    def __init__(self):
        self.enabled = True  # Toggle to disable all notifications

    # -------------------------
    # Core Notification Methods
    # -------------------------
    async def send_sms_notification(
        self,
        phone_number: str,
        message: str,
        template_id: Optional[str] = None
    ) -> dict:
        """
        Send SMS notification to a phone number.

        Args:
            phone_number: Customer phone number (with country code)
            message: SMS message content
            template_id: Optional template ID for template-based SMS

        Returns:
            dict with success status and message ID (placeholder)
        """
        if not self.enabled:
            logger.info(f"[SMS DISABLED] Would send to {phone_number}: {message[:50]}...")
            return {"success": True, "message_id": "placeholder_disabled", "provider": "sms"}

        # Placeholder - actual SMS provider integration here
        logger.info(f"[SMS PLACEHOLDER] To: {phone_number}")
        logger.info(f"[SMS PLACEHOLDER] Message: {message[:100]}...")

        return {
            "success": True,
            "message_id": f"sms_placeholder_{hash(phone_number + message) % 1000000}",
            "provider": "sms",
            "status": "sent_placeholder"
        }

    async def send_whatsapp_notification(
        self,
        phone_number: str,
        message: str,
        template_name: Optional[str] = None,
        template_params: Optional[dict] = None
    ) -> dict:
        """
        Send WhatsApp notification to a phone number.

        Args:
            phone_number: Customer phone number (with country code)
            message: WhatsApp message content
            template_name: Optional WhatsApp template name
            template_params: Optional template parameters

        Returns:
            dict with success status and message ID (placeholder)
        """
        if not self.enabled:
            logger.info(f"[WhatsApp DISABLED] Would send to {phone_number}: {message[:50]}...")
            return {"success": True, "message_id": "placeholder_disabled", "provider": "whatsapp"}

        # Placeholder - actual WhatsApp provider integration here
        logger.info(f"[WhatsApp PLACEHOLDER] To: {phone_number}")
        logger.info(f"[WhatsApp PLACEHOLDER] Message: {message[:100]}...")
        if template_name:
            logger.info(f"[WhatsApp PLACEHOLDER] Template: {template_name}, Params: {template_params}")

        return {
            "success": True,
            "message_id": f"wa_placeholder_{hash(phone_number + message) % 1000000}",
            "provider": "whatsapp",
            "status": "sent_placeholder"
        }

    async def send_notification(
        self,
        phone_number: str,
        message: str,
        preference: Literal["whatsapp", "sms", "both"] = "both",
        template_sms: Optional[str] = None,
        template_whatsapp: Optional[str] = None
    ) -> dict:
        """
        Send notification based on customer preference.

        Args:
            phone_number: Customer phone number
            message: Notification message
            preference: Customer notification preference (whatsapp, sms, or both)
            template_sms: Optional SMS template ID
            template_whatsapp: Optional WhatsApp template name

        Returns:
            dict with results for each channel
        """
        results = {
            "preference": preference,
            "phone_number": phone_number,
            "channels": {}
        }

        if preference in ["sms", "both"]:
            sms_result = await self.send_sms_notification(phone_number, message, template_sms)
            results["channels"]["sms"] = sms_result

        if preference in ["whatsapp", "both"]:
            wa_result = await self.send_whatsapp_notification(
                phone_number, message, template_whatsapp
            )
            results["channels"]["whatsapp"] = wa_result

        # Overall success if at least one channel succeeded
        results["success"] = any(
            ch.get("success", False) for ch in results["channels"].values()
        )

        return results


# ------------------------------------------------------------
# Service Request Notification Helpers
# ------------------------------------------------------------
class ServiceRequestNotificationHelper:
    """
    Helper class for sending service request related notifications.
    Provides pre-built messages for common service request events.
    """

    def __init__(self):
        self.notification_service = NotificationService()

    async def notify_request_created(
        self,
        phone_number: str,
        request_id: int,
        service_name: str,
        preference: Literal["whatsapp", "sms", "both"] = "both"
    ) -> dict:
        """
        Notify customer when service request is created.
        """
        message = (
            f"Your service request has been received!\n"
            f"Request ID: #{request_id}\n"
            f"Service: {service_name}\n\n"
            f"We will notify you once a provider is assigned."
        )

        return await self.notification_service.send_notification(
            phone_number=phone_number,
            message=message,
            preference=preference
        )

    async def notify_provider_assigned(
        self,
        phone_number: str,
        request_id: int,
        provider_name: str,
        service_name: str,
        preference: Literal["whatsapp", "sms", "both"] = "both"
    ) -> dict:
        """
        Notify customer when a provider is assigned.
        """
        message = (
            f"Good news! A provider has been assigned to your request.\n"
            f"Request ID: #{request_id}\n"
            f"Service: {service_name}\n"
            f"Provider: {provider_name}\n\n"
            f"They will contact you shortly."
        )

        return await self.notification_service.send_notification(
            phone_number=phone_number,
            message=message,
            preference=preference
        )

    async def notify_provider_accepted(
        self,
        phone_number: str,
        request_id: int,
        provider_name: str,
        preference: Literal["whatsapp", "sms", "both"] = "both"
    ) -> dict:
        """
        Notify customer when provider accepts the request.
        """
        message = (
            f"Your provider has accepted the request!\n"
            f"Request ID: #{request_id}\n"
            f"Provider: {provider_name}\n\n"
            f"They are on their way to serve you."
        )

        return await self.notification_service.send_notification(
            phone_number=phone_number,
            message=message,
            preference=preference
        )

    async def notify_service_completed(
        self,
        phone_number: str,
        request_id: int,
        provider_name: str,
        final_price: Optional[float] = None,
        preference: Literal["whatsapp", "sms", "both"] = "both"
    ) -> dict:
        """
        Notify customer when service is completed.
        """
        price_text = f"\nFinal Price: ${final_price:.2f}" if final_price else ""

        message = (
            f"Your service has been completed!\n"
            f"Request ID: #{request_id}\n"
            f"Provider: {provider_name}"
            f"{price_text}\n\n"
            f"Thank you for using our service."
        )

        return await self.notification_service.send_notification(
            phone_number=phone_number,
            message=message,
            preference=preference
        )

    async def notify_request_cancelled(
        self,
        phone_number: str,
        request_id: int,
        cancellation_reason: Optional[str] = None,
        preference: Literal["whatsapp", "sms", "both"] = "both"
    ) -> dict:
        """
        Notify customer when request is cancelled.
        """
        reason_text = f"\nReason: {cancellation_reason}" if cancellation_reason else ""

        message = (
            f"Your service request has been cancelled.\n"
            f"Request ID: #{request_id}"
            f"{reason_text}\n\n"
            f"If you have any questions, please contact support."
        )

        return await self.notification_service.send_notification(
            phone_number=phone_number,
            message=message,
            preference=preference
        )


# ------------------------------------------------------------
# Singleton Instances
# ------------------------------------------------------------
notification_service = NotificationService()
service_request_notifications = ServiceRequestNotificationHelper()
