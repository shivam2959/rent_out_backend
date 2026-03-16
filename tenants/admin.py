from django.contrib import admin
from .models import TenantOnboardingRequest


@admin.register(TenantOnboardingRequest)
class TenantOnboardingRequestAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'room', 'status', 'current_step', 'submitted_at', 'created_at']
    list_filter = ['status']
    search_fields = ['tenant__email', 'room__room_number']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at']
