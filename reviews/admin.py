from django.contrib import admin
from .models import BuildingReview, TenantReview


@admin.register(BuildingReview)
class BuildingReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'building', 'rating', 'is_verified_tenant', 'created_at')
    list_filter = ('rating', 'is_verified_tenant')
    search_fields = ('reviewer__email', 'building__name', 'title')


@admin.register(TenantReview)
class TenantReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'tenant', 'building', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('reviewer__email', 'tenant__email')
