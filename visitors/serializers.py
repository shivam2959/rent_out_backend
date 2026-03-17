from rest_framework import serializers
from .models import VisitorLog, EntryPass


class EntryPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryPass
        fields = '__all__'
        read_only_fields = ['pass_code', 'created_at']


class VisitorLogSerializer(serializers.ModelSerializer):
    entry_pass = EntryPassSerializer(read_only=True)

    class Meta:
        model = VisitorLog
        fields = '__all__'
        read_only_fields = ['tenant', 'created_at']
