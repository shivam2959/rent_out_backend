from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OwnerProfile, TenantProfile, LeaseOperatorProfile, BrokerProfile, SocietyManagerProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone')}),
    )
    list_display = ['username', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']

admin.site.register(OwnerProfile)
admin.site.register(TenantProfile)
admin.site.register(LeaseOperatorProfile)
admin.site.register(BrokerProfile)
admin.site.register(SocietyManagerProfile)
