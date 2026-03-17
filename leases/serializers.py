from rest_framework import serializers
from .models import LeaseAgreement, RentSchedule

class RentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentSchedule
        fields = '__all__'
        read_only_fields = ['lease']

class LeaseAgreementSerializer(serializers.ModelSerializer):
    rent_schedule = RentScheduleSerializer(read_only=True)

    class Meta:
        model = LeaseAgreement
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']
