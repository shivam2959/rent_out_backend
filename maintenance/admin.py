from django.contrib import admin
from .models import MaintenanceRequest


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'tenant', 'room', 'priority', 'status', 'assigned_to', 'created_at')
    list_filter = ('priority', 'status')
    search_fields = ('title', 'tenant__email', 'room__room_number', 'building__name')
    ordering = ('-created_at',)
