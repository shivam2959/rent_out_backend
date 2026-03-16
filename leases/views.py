from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import LeaseAgreement
from .serializers import LeaseAgreementSerializer
from users.permissions import IsOwnerOrAdmin


class LeaseAgreementViewSet(viewsets.ModelViewSet):
    serializer_class = LeaseAgreementSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LeaseAgreement.objects.select_related('tenant', 'room__building', 'owner').all()
        if user.role == 'owner':
            return LeaseAgreement.objects.select_related('tenant', 'room__building', 'owner').filter(owner=user)
        return LeaseAgreement.objects.select_related('tenant', 'room__building', 'owner').filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='sign-tenant')
    def sign_tenant(self, request, pk=None):
        lease = self.get_object()
        lease.signed_by_tenant = True
        if lease.signed_by_owner:
            lease.status = 'active'
        lease.save()
        return Response(LeaseAgreementSerializer(lease).data)

    @action(detail=True, methods=['post'], url_path='sign-owner')
    def sign_owner(self, request, pk=None):
        lease = self.get_object()
        lease.signed_by_owner = True
        if lease.signed_by_tenant:
            lease.status = 'active'
        lease.save()
        return Response(LeaseAgreementSerializer(lease).data)

    @action(detail=True, methods=['post'])
    def terminate(self, request, pk=None):
        lease = self.get_object()
        lease.status = 'terminated'
        lease.save()
        lease.room.is_available = True
        lease.room.save()
        return Response(LeaseAgreementSerializer(lease).data)
