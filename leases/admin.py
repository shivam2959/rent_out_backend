from django.contrib import admin
from .models import LeaseAgreement


@admin.register(LeaseAgreement)
class LeaseAgreementAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'room', 'status', 'start_date', 'end_date', 'monthly_rent', 'created_at']
    list_filter = ['status', 'tenant_signed', 'owner_signed']
    search_fields = ['tenant__email', 'room__room_number', 'room__building__name']
    readonly_fields = ['created_at', 'updated_at', 'tenant_signed_at', 'owner_signed_at']
