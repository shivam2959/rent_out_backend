from rest_framework import serializers
from .models import TenantOnboardingRequest

class TenantOnboardingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantOnboardingRequest
        fields = '__all__'
        read_only_fields = ['tenant', 'created_at', 'updated_at']
