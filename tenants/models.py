from django.db import models
from users.models import CustomUser
from properties.models import Room

class TenantOnboardingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='onboarding_requests')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='onboarding_requests')
    current_step = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Onboarding: {self.tenant.username} -> Room {self.room.room_number}"
