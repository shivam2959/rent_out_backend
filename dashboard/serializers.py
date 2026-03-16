from rest_framework import serializers

class OwnerDashboardSerializer(serializers.Serializer):
    total_buildings = serializers.IntegerField()
    total_rooms = serializers.IntegerField()
    available_rooms = serializers.IntegerField()
    occupied_rooms = serializers.IntegerField()
    active_leases = serializers.IntegerField()
    monthly_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    pending_maintenance = serializers.IntegerField()

class TenantDashboardSerializer(serializers.Serializer):
    active_lease = serializers.DictField(allow_null=True)
    pending_payments = serializers.IntegerField()
    total_payments = serializers.IntegerField()
    open_maintenance_requests = serializers.IntegerField()

class AdminDashboardSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_owners = serializers.IntegerField()
    total_tenants = serializers.IntegerField()
    total_buildings = serializers.IntegerField()
    total_rooms = serializers.IntegerField()
    active_leases = serializers.IntegerField()
    total_payments = serializers.IntegerField()
    pending_maintenance = serializers.IntegerField()
