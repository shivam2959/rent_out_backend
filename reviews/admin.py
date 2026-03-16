from django.contrib import admin
from .models import BuildingReview, TenantReview


@admin.register(BuildingReview)
class BuildingReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'building', 'rating', 'is_anonymous', 'created_at']
    list_filter = ['rating', 'is_anonymous']
    search_fields = ['reviewer__email', 'building__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TenantReview)
class TenantReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'tenant', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['reviewer__email', 'tenant__email']
    readonly_fields = ['created_at', 'updated_at']
