from rest_framework import serializers
from .models import MaintenanceRequest


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    tenant_email = serializers.CharField(source='tenant.email', read_only=True)
    room_info = serializers.SerializerMethodField()

    class Meta:
        model = MaintenanceRequest
        fields = '__all__'
        read_only_fields = ['tenant', 'resolved_at', 'created_at', 'updated_at']

    def get_room_info(self, obj) -> dict:
        return {
            'room_number': obj.room.room_number,
            'building': obj.room.building.name,
        }
