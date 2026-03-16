from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import MaintenanceRequest
from .serializers import MaintenanceRequestSerializer
from users.permissions import IsOwnerOrAdmin


class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceRequestSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'status', 'created_at']

    def get_permissions(self):
        if self.action in ['assign', 'resolve', 'close']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role == 'owner':
            queryset = MaintenanceRequest.objects.select_related(
                'tenant', 'room', 'building', 'assigned_to'
            ).all()
            if user.role == 'owner' and not user.is_staff:
                queryset = queryset.filter(building__owner=user)
        else:
            queryset = MaintenanceRequest.objects.select_related(
                'tenant', 'room', 'building', 'assigned_to'
            ).filter(tenant=user)
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        req_status = self.request.query_params.get('status')
        if req_status:
            queryset = queryset.filter(status=req_status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        maintenance = self.get_object()
        assigned_to_id = request.data.get('assigned_to')
        maintenance.assigned_to_id = assigned_to_id
        maintenance.status = 'in_progress'
        maintenance.save()
        return Response(MaintenanceRequestSerializer(maintenance).data)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        maintenance = self.get_object()
        maintenance.status = 'resolved'
        maintenance.resolved_at = timezone.now()
        maintenance.save()
        return Response(MaintenanceRequestSerializer(maintenance).data)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        maintenance = self.get_object()
        maintenance.status = 'closed'
        maintenance.save()
        return Response(MaintenanceRequestSerializer(maintenance).data)
