from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Building(models.Model):
    BUILDING_TYPES = [
        ('apartment', 'Apartment Complex'),
        ('house', 'Individual House'),
        ('villa', 'Villa'),
        ('commercial', 'Commercial Building'),
        ('pg', 'PG/Hostel'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buildings')
    name = models.CharField(max_length=255)
    building_type = models.CharField(max_length=20, choices=BUILDING_TYPES, default='apartment')
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    description = models.TextField(blank=True)
    total_floors = models.PositiveIntegerField(default=1)
    year_built = models.PositiveIntegerField(null=True, blank=True)
    # Amenities
    has_lift = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_security = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_swimming_pool = models.BooleanField(default=False)
    has_power_backup = models.BooleanField(default=False)
    has_water_supply = models.BooleanField(default=True)
    has_wifi = models.BooleanField(default=False)
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.city}"


class BuildingPhoto(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='building_photos/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.building.name}"


class Room(models.Model):
    ROOM_TYPES = [
        ('1bhk', '1 BHK'),
        ('2bhk', '2 BHK'),
        ('3bhk', '3 BHK'),
        ('studio', 'Studio'),
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('shop', 'Shop/Office'),
    ]

    FURNISHING_CHOICES = [
        ('unfurnished', 'Unfurnished'),
        ('semi_furnished', 'Semi Furnished'),
        ('fully_furnished', 'Fully Furnished'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
    ]

    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    floor_number = models.PositiveIntegerField(default=0)
    area_sqft = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    furnishing = models.CharField(max_length=20, choices=FURNISHING_CHOICES, default='unfurnished')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    # Pricing
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    maintenance_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    # Amenities
    has_ac = models.BooleanField(default=False)
    has_attached_bathroom = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['building', 'room_number']

    def __str__(self):
        return f"Room {self.room_number} - {self.building.name}"


class RoomPhoto(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='room_photos/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for Room {self.room.room_number}"
