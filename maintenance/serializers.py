from rest_framework import serializers
from .models import MaintenanceRequest


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    tenant_email = serializers.CharField(source='tenant.email', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    building_name = serializers.CharField(source='building.name', read_only=True)
    assigned_to_email = serializers.CharField(source='assigned_to.email', read_only=True)

    class Meta:
        model = MaintenanceRequest
        fields = ('id', 'tenant', 'tenant_email', 'room', 'room_number', 'building', 'building_name',
                  'title', 'description', 'priority', 'status', 'assigned_to', 'assigned_to_email',
                  'images', 'created_at', 'updated_at', 'resolved_at')
        read_only_fields = ('id', 'tenant', 'created_at', 'updated_at')
