from rest_framework import serializers
from .models import LeaseAgreement


class LeaseAgreementSerializer(serializers.ModelSerializer):
    tenant_email = serializers.CharField(source='tenant.email', read_only=True)
    room_info = serializers.SerializerMethodField()

    class Meta:
        model = LeaseAgreement
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at',
                            'tenant_signed_at', 'owner_signed_at']

    def get_room_info(self, obj) -> dict:
        return {
            'room_number': obj.room.room_number,
            'building': obj.room.building.name,
            'city': obj.room.building.city,
        }
