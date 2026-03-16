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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lease: {self.tenant.username} - Room {self.room.room_number} ({self.status})"
