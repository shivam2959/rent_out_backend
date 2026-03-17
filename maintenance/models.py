from django.db import models
from users.models import CustomUser
from properties.models import Room

class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='maintenance_requests')
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='maintenance_requests')
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_maintenance_requests',
        help_text="Technician or staff assigned to resolve the request",
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - Room {self.room.room_number} ({self.status})"


class MaintenanceComment(models.Model):
    """Progress notes / service history entries for a maintenance request."""
    request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='maintenance_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username} on Request {self.request_id}"
