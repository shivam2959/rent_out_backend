from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import TenantOnboardingRequest
from .serializers import TenantOnboardingRequestSerializer

class TenantOnboardingRequestViewSet(viewsets.ModelViewSet):
    serializer_class = TenantOnboardingRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ('owner', 'admin'):
            return TenantOnboardingRequest.objects.all()
        return TenantOnboardingRequest.objects.filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)
