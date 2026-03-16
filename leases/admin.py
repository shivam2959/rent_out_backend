from django.contrib import admin
from .models import LeaseAgreement


@admin.register(LeaseAgreement)
class LeaseAgreementAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'room', 'owner', 'status', 'start_date', 'end_date', 'monthly_rent')
    list_filter = ('status', 'signed_by_tenant', 'signed_by_owner')
    search_fields = ('tenant__email', 'owner__email', 'room__room_number')
    ordering = ('-created_at',)
