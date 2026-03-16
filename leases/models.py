from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LeaseAgreement(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
        ('renewed', 'Renewed'),
    ]

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lease_agreements')
    room = models.ForeignKey('properties.Room', on_delete=models.CASCADE, related_name='lease_agreements')
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit_paid = models.BooleanField(default=False)
    maintenance_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    agreement_document = models.FileField(upload_to='lease_agreements/', null=True, blank=True)
    terms_and_conditions = models.TextField(blank=True)
    # Damage tracking
    move_in_condition = models.TextField(blank=True)
    move_out_condition = models.TextField(blank=True)
    damage_description = models.TextField(blank=True)
    damage_amount_deducted = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Signatures
    tenant_signed = models.BooleanField(default=False)
    owner_signed = models.BooleanField(default=False)
    tenant_signed_at = models.DateTimeField(null=True, blank=True)
    owner_signed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='created_leases'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lease: {self.tenant.email} - Room {self.room.room_number}"
