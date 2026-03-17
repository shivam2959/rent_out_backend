"""
Helper functions for creating notifications from anywhere in the application.
Usage:
    from notifications_app.utils import notify
    notify(user, 'rent_reminder', 'Rent Due', 'Your rent of ₹5000 is due on 1st.', 'lease', lease.id)
"""
from .models import Notification


def notify(recipient, notification_type, title, message,
           related_object_type='', related_object_id=None):
    """Create a Notification for *recipient*."""
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        related_object_type=related_object_type,
        related_object_id=related_object_id,
    )
