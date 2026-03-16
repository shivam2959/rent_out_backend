from rest_framework import serializers
from .models import LeaseAgreement

class LeaseAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaseAgreement
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']
