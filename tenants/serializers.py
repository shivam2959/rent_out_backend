from rest_framework import serializers
from .models import TenantOnboardingRequest


class TenantOnboardingRequestSerializer(serializers.ModelSerializer):
    tenant_email = serializers.CharField(source='tenant.email', read_only=True)
    room_info = serializers.SerializerMethodField()

    class Meta:
        model = TenantOnboardingRequest
        fields = '__all__'
        read_only_fields = ['tenant', 'reviewed_by', 'submitted_at', 'created_at', 'updated_at']

    def get_room_info(self, obj):
        return {
            'room_number': obj.room.room_number,
            'building': obj.room.building.name,
            'monthly_rent': str(obj.room.monthly_rent)
        }


class OnboardingStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantOnboardingRequest
        fields = '__all__'
        read_only_fields = ['tenant', 'created_at', 'updated_at']
