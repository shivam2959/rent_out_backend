from django.db import models
from django.conf import settings


class LeaseAgreement(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ]
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tenant_leases')
    room = models.ForeignKey('properties.Room', on_delete=models.CASCADE, related_name='leases')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner_leases')
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    terms_and_conditions = models.TextField(blank=True, null=True)
    signed_by_tenant = models.BooleanField(default=False)
    signed_by_owner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Lease: {self.tenant.email} - Room {self.room.room_number} ({self.status})"

    @property
    def is_fully_signed(self):
        return self.signed_by_tenant and self.signed_by_owner
