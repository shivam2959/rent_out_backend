from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import TenantOnboardingRequest
from .serializers import TenantOnboardingRequestSerializer, StepUpdateSerializer
from users.permissions import IsTenantOrAdmin, IsOwnerOrAdmin


class TenantOnboardingViewSet(viewsets.ModelViewSet):
    serializer_class = TenantOnboardingRequestSerializer

    def get_permissions(self):
        if self.action in ['approve', 'reject']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role == 'owner':
            return TenantOnboardingRequest.objects.select_related('tenant', 'room__building').all()
        return TenantOnboardingRequest.objects.select_related('tenant', 'room__building').filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    @action(detail=True, methods=['post'], url_path='next-step')
    def next_step(self, request, pk=None):
        onboarding = self.get_object()
        if onboarding.status in ('approved', 'rejected'):
            return Response({'error': 'Application already finalized.'}, status=status.HTTP_400_BAD_REQUEST)
        step_map = {1: 'step_1', 2: 'step_2', 3: 'step_3', 4: 'step_4', 5: 'step_5', 6: 'step_6', 7: 'step_7'}
        current = onboarding.current_step
        if current < 7:
            onboarding.status = step_map.get(current + 1, 'step_7')
            onboarding.current_step += 1
            if 'personal_info' in request.data:
                onboarding.personal_info = request.data['personal_info']
            if 'references' in request.data:
                onboarding.references = request.data['references']
            for field in ['id_proof', 'address_proof', 'employment_proof']:
                if field in request.FILES:
                    setattr(onboarding, field, request.FILES[field])
            onboarding.save()
        return Response(TenantOnboardingRequestSerializer(onboarding).data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        onboarding = self.get_object()
        onboarding.status = 'approved'
        onboarding.notes = request.data.get('notes', onboarding.notes)
        onboarding.save()
        onboarding.room.is_available = False
        onboarding.room.save()
        return Response(TenantOnboardingRequestSerializer(onboarding).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        onboarding = self.get_object()
        onboarding.status = 'rejected'
        onboarding.notes = request.data.get('notes', onboarding.notes)
        onboarding.save()
        return Response(TenantOnboardingRequestSerializer(onboarding).data)


class MyRoomsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TenantOnboardingRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TenantOnboardingRequest.objects.filter(
            tenant=self.request.user, status='approved'
        ).select_related('room__building')
