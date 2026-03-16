from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MaintenanceRequest(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ]

    CATEGORY_CHOICES = [
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('carpentry', 'Carpentry'),
        ('painting', 'Painting'),
        ('cleaning', 'Cleaning'),
        ('pest_control', 'Pest Control'),
        ('appliance', 'Appliance Repair'),
        ('internet', 'Internet/WiFi'),
        ('other', 'Other'),
    ]

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maintenance_requests')
    room = models.ForeignKey('properties.Room', on_delete=models.CASCADE, related_name='maintenance_requests')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    photo = models.ImageField(upload_to='maintenance_photos/', null=True, blank=True)
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_maintenance'
    )
    resolution_notes = models.TextField(blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maintenance: {self.title} - Room {self.room.room_number} ({self.status})"
