from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OwnerProfile, TenantProfile, LeaseOperatorProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_verified', 'is_active', 'created_at')
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'profile_photo', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('email', 'role', 'phone_number')}),
    )


@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'pan_number', 'created_at')
    search_fields = ('user__email', 'company_name', 'pan_number')


@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'occupation', 'emergency_contact_name', 'created_at')
    search_fields = ('user__email', 'occupation')


@admin.register(LeaseOperatorProfile)
class LeaseOperatorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'license_number', 'created_at')
    search_fields = ('user__email', 'company_name', 'license_number')
