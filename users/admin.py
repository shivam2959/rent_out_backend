from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OwnerProfile, TenantProfile, LeaseOperatorProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'role', 'is_verified', 'is_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number', 'profile_picture', 'is_verified')}),
    )


@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'pan_number', 'bank_name', 'kyc_verified', 'created_at']
    list_filter = ['kyc_verified']
    search_fields = ['user__email', 'pan_number']


@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'occupation', 'is_verified', 'created_at']
    list_filter = ['is_verified']
    search_fields = ['user__email', 'occupation']


@admin.register(LeaseOperatorProfile)
class LeaseOperatorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'is_verified', 'created_at']
    list_filter = ['is_verified']
    search_fields = ['user__email', 'company_name']
