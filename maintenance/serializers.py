from rest_framework import serializers
from .models import MaintenanceRequest, MaintenanceComment

class MaintenanceCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceComment
        fields = '__all__'
        read_only_fields = ['commenter', 'created_at']

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    comments = MaintenanceCommentSerializer(many=True, read_only=True)

    class Meta:
        model = MaintenanceRequest
        fields = '__all__'
        read_only_fields = ['tenant', 'created_at', 'updated_at']
