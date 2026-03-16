from django.contrib import admin
from .models import Amenity, Building, BuildingPhoto, Room, RoomPhoto

admin.site.register(Amenity)
admin.site.register(Building)
admin.site.register(BuildingPhoto)
admin.site.register(Room)
admin.site.register(RoomPhoto)
