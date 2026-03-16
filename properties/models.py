from django.db import models
from users.models import CustomUser

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Building(models.Model):
    BUILDING_TYPES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed', 'Mixed Use'),
    ]
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buildings')
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    building_type = models.CharField(max_length=20, choices=BUILDING_TYPES, default='residential')
    total_floors = models.PositiveIntegerField(default=1)
    amenities = models.ManyToManyField(Amenity, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

class BuildingPhoto(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='buildings/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Photo for {self.building.name}"

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('studio', 'Studio'),
        ('1bhk', '1 BHK'),
        ('2bhk', '2 BHK'),
        ('3bhk', '3 BHK'),
        ('commercial', 'Commercial'),
    ]
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    floor = models.PositiveIntegerField(default=0)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='single')
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    area_sqft = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.room_number} - {self.building.name}"

class RoomPhoto(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='rooms/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Photo for Room {self.room.room_number}"
