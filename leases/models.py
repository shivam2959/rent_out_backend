from django.db import models
from users.models import CustomUser
from properties.models import Room

class LeaseAgreement(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ]
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leases_as_tenant')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='leases')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leases_as_owner')
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    terms = models.TextField(blank=True)
    notice_period_days = models.PositiveIntegerField(default=30)
    is_digital = models.BooleanField(default=False, help_text="Whether agreement was signed digitally")
    signed_by_tenant_at = models.DateTimeField(null=True, blank=True)
    signed_by_owner_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lease: {self.tenant.username} - Room {self.room.room_number} ({self.status})"


class RentSchedule(models.Model):
    """Defines the recurring rent cycle for a lease."""
    lease = models.OneToOneField(LeaseAgreement, on_delete=models.CASCADE, related_name='rent_schedule')
    due_day_of_month = models.PositiveSmallIntegerField(
        default=1, help_text="Day of month rent is due (1–28)"
    )
    grace_period_days = models.PositiveSmallIntegerField(default=5)
    late_penalty_per_day = models.DecimalField(
        max_digits=8, decimal_places=2, default=0,
        help_text="Extra charge per day after grace period"
    )

    def __str__(self):
        return f"RentSchedule for Lease {self.lease_id} – due day {self.due_day_of_month}"
