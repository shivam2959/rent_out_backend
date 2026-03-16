from rest_framework import serializers


class OwnerDashboardSerializer(serializers.Serializer):
    total_buildings = serializers.IntegerField()
    total_rooms = serializers.IntegerField()
    available_rooms = serializers.IntegerField()
    occupied_rooms = serializers.IntegerField()
    total_tenants = serializers.IntegerField()
    payments_this_month = serializers.DecimalField(max_digits=12, decimal_places=2)
    pending_maintenance = serializers.IntegerField()
    active_leases = serializers.IntegerField()


class TenantDashboardSerializer(serializers.Serializer):
    current_room = serializers.DictField(allow_null=True)
    lease_info = serializers.DictField(allow_null=True)
    pending_payments = serializers.IntegerField()
    maintenance_requests = serializers.IntegerField()
    total_paid_this_month = serializers.DecimalField(max_digits=12, decimal_places=2)


class AnalyticsDashboardSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_owners = serializers.IntegerField()
    total_tenants = serializers.IntegerField()
    total_buildings = serializers.IntegerField()
    total_rooms = serializers.IntegerField()
    total_active_leases = serializers.IntegerField()
    total_payments = serializers.DecimalField(max_digits=14, decimal_places=2)
    open_maintenance_requests = serializers.IntegerField()
