from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import LeaseAgreement
from .serializers import LeaseAgreementSerializer


class LeaseAgreementViewSet(viewsets.ModelViewSet):
    queryset = LeaseAgreement.objects.all()
    serializer_class = LeaseAgreementSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['tenant__email', 'room__room_number', 'room__building__name']
    ordering_fields = ['start_date', 'end_date', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LeaseAgreement.objects.all().select_related('tenant', 'room', 'room__building')
        return LeaseAgreement.objects.filter(
            Q(tenant=user) | Q(room__building__owner=user)
        ).select_related('tenant', 'room', 'room__building')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def sign_tenant(self, request, pk=None):
        lease = self.get_object()
        if lease.tenant != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        lease.tenant_signed = True
        lease.tenant_signed_at = timezone.now()
        lease.save()
        return Response({'status': 'signed'})

    @action(detail=True, methods=['post'])
    def sign_owner(self, request, pk=None):
        lease = self.get_object()
        if lease.room.building.owner != request.user and not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        lease.owner_signed = True
        lease.owner_signed_at = timezone.now()
        if lease.tenant_signed:
            lease.status = 'active'
            lease.room.status = 'occupied'
            lease.room.save()
        lease.save()
        return Response({'status': 'signed'})

    @action(detail=True, methods=['post'])
    def terminate(self, request, pk=None):
        lease = self.get_object()
        lease.status = 'terminated'
        lease.move_out_condition = request.data.get('move_out_condition', '')
        lease.damage_description = request.data.get('damage_description', '')
        lease.damage_amount_deducted = request.data.get('damage_amount_deducted', 0)
        lease.room.status = 'available'
        lease.room.save()
        lease.save()
        return Response({'status': 'terminated'})
