from django.db import models
from users.models import CustomUser


class Notification(models.Model):
    TYPE_CHOICES = [
        ('rent_reminder', 'Rent Reminder'),
        ('rent_overdue', 'Rent Overdue'),
        ('lease_expiry', 'Lease Expiry'),
        ('lease_renewal', 'Lease Renewal'),
        ('maintenance_update', 'Maintenance Update'),
        ('visitor_approval', 'Visitor Approval'),
        ('visitor_checkin', 'Visitor Check-In'),
        ('subscription_renewal', 'Subscription Renewal'),
        ('subscription_overdue', 'Subscription Overdue'),
        ('kyc_update', 'KYC Status Update'),
        ('vacancy_application', 'Vacancy Application'),
        ('general', 'General'),
    ]
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='notifications'
    )
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='general')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    # Optional generic link back to the source object (e.g. lease id, payment id)
    related_object_type = models.CharField(max_length=100, blank=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.notification_type}] {self.title} → {self.recipient.username}"
