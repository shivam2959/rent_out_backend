from django.contrib import admin
from .models import Amenity, Building, BuildingPhoto, Floor, Room, RoomPhoto

admin.site.register(Amenity)
admin.site.register(Building)
admin.site.register(BuildingPhoto)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(RoomPhoto)
