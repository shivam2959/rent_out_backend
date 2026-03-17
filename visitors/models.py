import uuid
from django.db import models
from users.models import CustomUser
from properties.models import Room


class VisitorLog(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='visitor_logs')
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='visitor_logs')
    visitor_name = models.CharField(max_length=200)
    visitor_phone = models.CharField(max_length=20, blank=True)
    purpose = models.CharField(max_length=200, blank=True)
    expected_arrival = models.DateTimeField()
    actual_arrival = models.DateTimeField(null=True, blank=True)
    departure = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visitor {self.visitor_name} → Room {self.room.room_number} ({self.status})"


class EntryPass(models.Model):
    visitor_log = models.OneToOneField(VisitorLog, on_delete=models.CASCADE, related_name='entry_pass')
    pass_code = models.CharField(max_length=20, unique=True, blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pass_code:
            self.pass_code = f"EP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"EntryPass {self.pass_code} for {self.visitor_log.visitor_name}"
