from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OwnerDashboardSerializer, TenantDashboardSerializer, AnalyticsDashboardSerializer
from users.permissions import IsOwnerOrAdmin, IsTenantOrAdmin


class OwnerDashboardView(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def get(self, request):
        from properties.models import Building, Room
        from leases.models import LeaseAgreement
        from payments.models import Payment
        from maintenance.models import MaintenanceRequest
        from django.db.models import Sum

        now = timezone.now()

        buildings = Building.objects.filter(owner=request.user)
        building_ids = buildings.values_list('id', flat=True)
        rooms = Room.objects.filter(building__in=building_ids)
        room_ids = rooms.values_list('id', flat=True)

        tenant_ids = LeaseAgreement.objects.filter(
            room__in=room_ids, status='active'
        ).values_list('tenant', flat=True).distinct()

        payments_this_month = Payment.objects.filter(
            lease__room__in=room_ids,
            status='completed',
            payment_date__year=now.year,
            payment_date__month=now.month,
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        data = {
            'total_buildings': buildings.count(),
            'total_rooms': rooms.count(),
            'available_rooms': rooms.filter(is_available=True).count(),
            'occupied_rooms': rooms.filter(is_available=False).count(),
            'total_tenants': len(tenant_ids),
            'payments_this_month': payments_this_month,
            'pending_maintenance': MaintenanceRequest.objects.filter(
                building__in=building_ids, status='open'
            ).count(),
            'active_leases': LeaseAgreement.objects.filter(
                room__in=room_ids, status='active'
            ).count(),
        }
        serializer = OwnerDashboardSerializer(data)
        return Response(serializer.data)


class TenantDashboardView(APIView):
    permission_classes = [IsTenantOrAdmin]

    def get(self, request):
        from leases.models import LeaseAgreement
        from payments.models import Payment
        from maintenance.models import MaintenanceRequest
        from django.db.models import Sum

        now = timezone.now()

        active_lease = LeaseAgreement.objects.filter(
            tenant=request.user, status='active'
        ).select_related('room__building').first()

        current_room = None
        lease_info = None
        if active_lease:
            current_room = {
                'room_number': active_lease.room.room_number,
                'building_name': active_lease.room.building.name,
                'city': active_lease.room.building.city,
                'rent_amount': str(active_lease.room.rent_amount),
            }
            lease_info = {
                'id': active_lease.id,
                'start_date': str(active_lease.start_date),
                'end_date': str(active_lease.end_date),
                'monthly_rent': str(active_lease.monthly_rent),
                'status': active_lease.status,
            }

        total_paid_this_month = Payment.objects.filter(
            tenant=request.user,
            status='completed',
            payment_date__year=now.year,
            payment_date__month=now.month,
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        data = {
            'current_room': current_room,
            'lease_info': lease_info,
            'pending_payments': Payment.objects.filter(tenant=request.user, status='pending').count(),
            'maintenance_requests': MaintenanceRequest.objects.filter(
                tenant=request.user, status__in=['open', 'in_progress']
            ).count(),
            'total_paid_this_month': total_paid_this_month,
        }
        serializer = TenantDashboardSerializer(data)
        return Response(serializer.data)


class AnalyticsDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        from django.contrib.auth import get_user_model
        from properties.models import Building, Room
        from leases.models import LeaseAgreement
        from payments.models import Payment
        from maintenance.models import MaintenanceRequest
        from django.db.models import Sum

        User = get_user_model()

        total_payments = Payment.objects.filter(
            status='completed'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        data = {
            'total_users': User.objects.count(),
            'total_owners': User.objects.filter(role='owner').count(),
            'total_tenants': User.objects.filter(role='tenant').count(),
            'total_buildings': Building.objects.count(),
            'total_rooms': Room.objects.count(),
            'total_active_leases': LeaseAgreement.objects.filter(status='active').count(),
            'total_payments': total_payments,
            'open_maintenance_requests': MaintenanceRequest.objects.filter(status='open').count(),
        }
        serializer = AnalyticsDashboardSerializer(data)
        return Response(serializer.data)
