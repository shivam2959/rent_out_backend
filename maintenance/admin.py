from django.contrib import admin
from .models import MaintenanceRequest


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'tenant', 'room', 'category', 'priority', 'status', 'created_at']
    list_filter = ['status', 'priority', 'category']
    search_fields = ['title', 'tenant__email', 'room__room_number']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at']
