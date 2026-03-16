from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import MaintenanceRequest
from .serializers import MaintenanceRequestSerializer


class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title', 'description', 'tenant__email', 'room__room_number']
    ordering_fields = ['created_at', 'priority', 'status']
    filterset_fields = ['status', 'priority', 'category', 'room']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MaintenanceRequest.objects.all().select_related('tenant', 'room', 'room__building')
        return MaintenanceRequest.objects.filter(
            Q(tenant=user) | Q(room__building__owner=user)
        ).select_related('tenant', 'room', 'room__building')

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        maintenance = self.get_object()
        maintenance.status = 'resolved'
        maintenance.resolution_notes = request.data.get('resolution_notes', '')
        maintenance.actual_cost = request.data.get('actual_cost')
        maintenance.resolved_at = timezone.now()
        maintenance.save()
        return Response({'status': 'resolved'})

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        maintenance = self.get_object()
        maintenance.assigned_to_id = request.data.get('assigned_to')
        maintenance.status = 'in_progress'
        maintenance.scheduled_date = request.data.get('scheduled_date')
        maintenance.save()
        return Response({'status': 'assigned'})
