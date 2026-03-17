from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import VisitorLog, EntryPass
from .serializers import VisitorLogSerializer, EntryPassSerializer


class VisitorLogViewSet(viewsets.ModelViewSet):
    serializer_class = VisitorLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ('owner', 'admin', 'society_manager'):
            return VisitorLog.objects.filter(room__building__owner=user)
        return VisitorLog.objects.filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        log = self.get_object()
        log.status = 'approved'
        log.save()
        from datetime import timedelta
        valid_until = log.expected_arrival + timedelta(hours=24)
        pass_obj, _ = EntryPass.objects.get_or_create(
            visitor_log=log,
            defaults={
                'valid_from': log.expected_arrival,
                'valid_until': valid_until,
            },
        )
        return Response({
            'visitor_log': VisitorLogSerializer(log).data,
            'entry_pass': EntryPassSerializer(pass_obj).data,
        })

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        log = self.get_object()
        log.status = 'rejected'
        log.save()
        return Response(VisitorLogSerializer(log).data)

    @action(detail=True, methods=['post'])
    def checkin(self, request, pk=None):
        from django.utils import timezone
        log = self.get_object()
        log.status = 'checked_in'
        log.actual_arrival = timezone.now()
        log.save()
        return Response(VisitorLogSerializer(log).data)

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        from django.utils import timezone
        log = self.get_object()
        log.status = 'checked_out'
        log.departure = timezone.now()
        log.save()
        return Response(VisitorLogSerializer(log).data)
