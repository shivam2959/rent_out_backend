from rest_framework import serializers
from .models import TenantOnboardingRequest


class TenantOnboardingRequestSerializer(serializers.ModelSerializer):
    tenant_email = serializers.CharField(source='tenant.email', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    building_name = serializers.CharField(source='room.building.name', read_only=True)

    class Meta:
        model = TenantOnboardingRequest
        fields = ('id', 'tenant', 'tenant_email', 'room', 'room_number', 'building_name',
                  'status', 'personal_info', 'id_proof', 'address_proof', 'employment_proof',
                  'references', 'current_step', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'tenant', 'status', 'current_step', 'created_at', 'updated_at')
