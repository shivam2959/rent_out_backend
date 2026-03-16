from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from users.permissions import IsOwner, IsTenant, IsOwnerOrAdmin
from properties.models import Building, Room
from leases.models import LeaseAgreement
from payments.models import Payment
from maintenance.models import MaintenanceRequest

class OwnerDashboardView(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        user = request.user
        buildings = Building.objects.filter(owner=user)
        rooms = Room.objects.filter(building__owner=user)
        active_leases = LeaseAgreement.objects.filter(owner=user, status='active')
        monthly_revenue = sum(
            lease.monthly_rent for lease in active_leases
        )
        pending_maintenance = MaintenanceRequest.objects.filter(
            room__building__owner=user, status='pending'
        ).count()
        return Response({
            'total_buildings': buildings.count(),
            'total_rooms': rooms.count(),
            'available_rooms': rooms.filter(is_available=True).count(),
            'occupied_rooms': rooms.filter(is_available=False).count(),
            'active_leases': active_leases.count(),
            'monthly_revenue': str(monthly_revenue),
            'pending_maintenance': pending_maintenance,
        })

class TenantDashboardView(APIView):
    permission_classes = [IsTenant]

    def get(self, request):
        user = request.user
        active_lease = LeaseAgreement.objects.filter(tenant=user, status='active').first()
        lease_data = None
        if active_lease:
            lease_data = {
                'id': active_lease.id,
                'room': active_lease.room.room_number,
                'building': active_lease.room.building.name,
                'monthly_rent': str(active_lease.monthly_rent),
                'start_date': str(active_lease.start_date),
                'end_date': str(active_lease.end_date),
            }
        payments = Payment.objects.filter(lease__tenant=user)
        open_maintenance = MaintenanceRequest.objects.filter(
            tenant=user, status__in=['pending', 'in_progress']
        ).count()
        return Response({
            'active_lease': lease_data,
            'pending_payments': payments.filter(status='pending').count(),
            'total_payments': payments.count(),
            'open_maintenance_requests': open_maintenance,
        })

class AdminDashboardView(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def get(self, request):
        return Response({
            'total_users': CustomUser.objects.count(),
            'total_owners': CustomUser.objects.filter(role='owner').count(),
            'total_tenants': CustomUser.objects.filter(role='tenant').count(),
            'total_buildings': Building.objects.count(),
            'total_rooms': Room.objects.count(),
            'active_leases': LeaseAgreement.objects.filter(status='active').count(),
            'total_payments': Payment.objects.count(),
            'pending_maintenance': MaintenanceRequest.objects.filter(status='pending').count(),
        })
