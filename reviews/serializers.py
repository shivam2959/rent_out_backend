from rest_framework import serializers
from .models import BuildingReview, TenantReview


class BuildingReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = BuildingReview
        fields = '__all__'
        read_only_fields = ['reviewer', 'created_at', 'updated_at']

    def get_reviewer_name(self, obj):
        if obj.is_anonymous:
            return 'Anonymous'
        return obj.reviewer.get_full_name() or obj.reviewer.email


class TenantReviewSerializer(serializers.ModelSerializer):
    reviewer_email = serializers.CharField(source='reviewer.email', read_only=True)
    tenant_email = serializers.CharField(source='tenant.email', read_only=True)

    class Meta:
        model = TenantReview
        fields = '__all__'
        read_only_fields = ['reviewer', 'created_at', 'updated_at']
