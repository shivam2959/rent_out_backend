from django.contrib import admin
from .models import Building, Room, BuildingPhoto, RoomPhoto


class BuildingPhotoInline(admin.TabularInline):
    model = BuildingPhoto
    extra = 1


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0
    show_change_link = True


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'state', 'is_active', 'total_floors', 'created_at')
    list_filter = ('is_active', 'city', 'state')
    search_fields = ('name', 'city', 'address', 'owner__email')
    inlines = [BuildingPhotoInline, RoomInline]


class RoomPhotoInline(admin.TabularInline):
    model = RoomPhoto
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'building', 'room_type', 'floor', 'rent_amount', 'is_available')
    list_filter = ('room_type', 'is_available', 'floor')
    search_fields = ('room_number', 'building__name')
    inlines = [RoomPhotoInline]
