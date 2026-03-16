from django.contrib import admin
from .models import TenantOnboardingRequest


@admin.register(TenantOnboardingRequest)
class TenantOnboardingRequestAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'room', 'status', 'current_step', 'created_at')
    list_filter = ('status',)
    search_fields = ('tenant__email', 'room__room_number', 'room__building__name')
    ordering = ('-created_at',)
