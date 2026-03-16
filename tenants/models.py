from django.db import models
from django.conf import settings


class TenantOnboardingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('step_1', 'Step 1 - Personal Info'),
        ('step_2', 'Step 2 - ID Proof'),
        ('step_3', 'Step 3 - Address Proof'),
        ('step_4', 'Step 4 - Employment Proof'),
        ('step_5', 'Step 5 - References'),
        ('step_6', 'Step 6 - Review'),
        ('step_7', 'Step 7 - Final'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='onboarding_requests')
    room = models.ForeignKey('properties.Room', on_delete=models.CASCADE, related_name='onboarding_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    personal_info = models.JSONField(default=dict, blank=True)
    id_proof = models.FileField(upload_to='tenant_docs/id_proofs/', blank=True, null=True)
    address_proof = models.FileField(upload_to='tenant_docs/address_proofs/', blank=True, null=True)
    employment_proof = models.FileField(upload_to='tenant_docs/employment_proofs/', blank=True, null=True)
    references = models.JSONField(default=list, blank=True)
    current_step = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Onboarding: {self.tenant.email} -> Room {self.room.room_number}"
