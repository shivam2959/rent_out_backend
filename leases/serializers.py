from rest_framework import serializers
from .models import LeaseAgreement


class LeaseAgreementSerializer(serializers.ModelSerializer):
    tenant_email = serializers.CharField(source='tenant.email', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    building_name = serializers.CharField(source='room.building.name', read_only=True)
    is_fully_signed = serializers.ReadOnlyField()

    class Meta:
        model = LeaseAgreement
        fields = ('id', 'tenant', 'tenant_email', 'room', 'room_number', 'building_name',
                  'owner', 'owner_email', 'start_date', 'end_date', 'monthly_rent',
                  'security_deposit', 'status', 'terms_and_conditions',
                  'signed_by_tenant', 'signed_by_owner', 'is_fully_signed',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
