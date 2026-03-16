from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import TenantOnboardingRequest
from .serializers import TenantOnboardingRequestSerializer, OnboardingStepSerializer
from users.permissions import IsTenantOrAdmin


class TenantOnboardingRequestViewSet(viewsets.ModelViewSet):
    queryset = TenantOnboardingRequest.objects.all()
    serializer_class = TenantOnboardingRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['created_at', 'status']
    search_fields = ['tenant__email', 'room__room_number']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TenantOnboardingRequest.objects.all().select_related('tenant', 'room', 'room__building')
        return TenantOnboardingRequest.objects.filter(tenant=user).select_related('room', 'room__building')

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        onboarding = self.get_object()
        onboarding.status = 'approved'
        onboarding.reviewed_by = request.user
        onboarding.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        onboarding = self.get_object()
        onboarding.status = 'rejected'
        onboarding.reviewed_by = request.user
        onboarding.review_notes = request.data.get('notes', '')
        onboarding.save()
        return Response({'status': 'rejected'})

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        onboarding = self.get_object()
        if onboarding.tenant != request.user and not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        onboarding.status = 'pending'
        onboarding.terms_accepted = True
        onboarding.submitted_at = timezone.now()
        onboarding.save()
        return Response({'status': 'submitted'})
