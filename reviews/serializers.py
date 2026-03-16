from rest_framework import serializers
from .models import BuildingReview, TenantReview


class BuildingReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.full_name', read_only=True)
    building_name = serializers.CharField(source='building.name', read_only=True)

    class Meta:
        model = BuildingReview
        fields = ('id', 'reviewer', 'reviewer_name', 'building', 'building_name',
                  'rating', 'title', 'content', 'is_verified_tenant', 'created_at')
        read_only_fields = ('id', 'reviewer', 'is_verified_tenant', 'created_at')


class TenantReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.full_name', read_only=True)
    tenant_name = serializers.CharField(source='tenant.full_name', read_only=True)

    class Meta:
        model = TenantReview
        fields = ('id', 'reviewer', 'reviewer_name', 'tenant', 'tenant_name',
                  'building', 'rating', 'content', 'created_at')
        read_only_fields = ('id', 'reviewer', 'created_at')
