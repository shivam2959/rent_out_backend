from django.db import models
from properties.models import Room


class InventoryItem(models.Model):
    CATEGORY_CHOICES = [
        ('furniture', 'Furniture'),
        ('appliance', 'Appliance'),
        ('electronics', 'Electronics'),
        ('fixture', 'Fixture / Fitting'),
        ('other', 'Other'),
    ]
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('damaged', 'Damaged'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='inventory_items')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='furniture')
    serial_number = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    purchase_date = models.DateField(null=True, blank=True)
    purchase_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()}) – Room {self.room.room_number}"
