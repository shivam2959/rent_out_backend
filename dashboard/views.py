from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta


class DashboardSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {}

        if user.is_staff or user.role == 'owner':
            from properties.models import Building, Room
            from payments.models import Payment
            from maintenance.models import MaintenanceRequest

            if user.is_staff:
                buildings = Building.objects.filter(is_active=True)
            else:
                buildings = Building.objects.filter(owner=user, is_active=True)

            building_ids = buildings.values_list('id', flat=True)
            rooms = Room.objects.filter(building__in=building_ids)

            data['buildings_count'] = buildings.count()
            data['total_rooms'] = rooms.count()
            data['occupied_rooms'] = rooms.filter(status='occupied').count()
            data['available_rooms'] = rooms.filter(status='available').count()

            current_month = timezone.now().replace(day=1)
            if user.is_staff:
                monthly_revenue = Payment.objects.filter(
                    status='completed',
                    payment_date__gte=current_month
                ).aggregate(total=Sum('amount'))['total'] or 0
            else:
                monthly_revenue = Payment.objects.filter(
                    lease__room__building__owner=user,
                    status='completed',
                    payment_date__gte=current_month
                ).aggregate(total=Sum('amount'))['total'] or 0

            data['monthly_revenue'] = monthly_revenue

            pending_maintenance = MaintenanceRequest.objects.filter(
                room__building__in=building_ids,
                status__in=['open', 'in_progress']
            ).count()
            data['pending_maintenance'] = pending_maintenance

        if user.role == 'tenant':
            from leases.models import LeaseAgreement
            from payments.models import Payment
            from maintenance.models import MaintenanceRequest

            active_lease = LeaseAgreement.objects.filter(
                tenant=user, status='active'
            ).first()
            data['active_lease'] = active_lease.id if active_lease else None

            pending_payments = Payment.objects.filter(
                tenant=user, status='pending'
            ).count()
            data['pending_payments'] = pending_payments

            my_maintenance = MaintenanceRequest.objects.filter(
                tenant=user, status__in=['open', 'in_progress']
            ).count()
            data['open_maintenance_requests'] = my_maintenance

        return Response(data)


class RevenueReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from payments.models import Payment
        user = request.user

        if user.is_staff:
            payments = Payment.objects.filter(status='completed')
        elif user.role == 'owner':
            payments = Payment.objects.filter(
                lease__room__building__owner=user,
                status='completed'
            )
        else:
            return Response({'error': 'Permission denied'}, status=403)

        last_6_months = []
        for i in range(5, -1, -1):
            month_start = (timezone.now() - timedelta(days=30 * i)).replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            if i > 0:
                month_end = (timezone.now() - timedelta(days=30 * (i - 1))).replace(
                    day=1, hour=0, minute=0, second=0, microsecond=0
                )
            else:
                month_end = timezone.now()

            month_revenue = payments.filter(
                payment_date__gte=month_start,
                payment_date__lt=month_end
            ).aggregate(total=Sum('amount'))['total'] or 0

            last_6_months.append({
                'month': month_start.strftime('%B %Y'),
                'revenue': month_revenue
            })

        return Response({'monthly_revenue': last_6_months})
