from rest_framework import serializers
from .models import BuildingReview, TenantReview

class BuildingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingReview
        fields = '__all__'
        read_only_fields = ['tenant', 'created_at']

class TenantReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantReview
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']
