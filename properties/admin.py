from django.contrib import admin
from .models import Building, BuildingPhoto, Room, RoomPhoto


class BuildingPhotoInline(admin.TabularInline):
    model = BuildingPhoto
    extra = 1


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0
    fields = ['room_number', 'room_type', 'status', 'monthly_rent']


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'building_type', 'city', 'state', 'is_active', 'created_at']
    list_filter = ['building_type', 'is_active', 'city', 'state']
    search_fields = ['name', 'city', 'address', 'owner__email']
    inlines = [BuildingPhotoInline, RoomInline]


class RoomPhotoInline(admin.TabularInline):
    model = RoomPhoto
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'building', 'room_type', 'status', 'monthly_rent', 'created_at']
    list_filter = ['status', 'room_type', 'furnishing', 'is_active']
    search_fields = ['room_number', 'building__name']
    inlines = [RoomPhotoInline]
