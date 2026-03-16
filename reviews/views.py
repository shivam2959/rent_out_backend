from rest_framework import viewsets, permissions
from .models import BuildingReview, TenantReview
from .serializers import BuildingReviewSerializer, TenantReviewSerializer


class BuildingReviewViewSet(viewsets.ModelViewSet):
    queryset = BuildingReview.objects.all()
    serializer_class = BuildingReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['building__name', 'review']
    ordering_fields = ['rating', 'created_at']
    filterset_fields = ['building', 'rating']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def get_queryset(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return BuildingReview.objects.filter(reviewer=self.request.user)
        return BuildingReview.objects.all().select_related('reviewer', 'building')


class TenantReviewViewSet(viewsets.ModelViewSet):
    queryset = TenantReview.objects.all()
    serializer_class = TenantReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['tenant__email', 'review']
    ordering_fields = ['rating', 'created_at']

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TenantReview.objects.all().select_related('reviewer', 'tenant', 'lease')
        return TenantReview.objects.filter(
            reviewer=user
        ).select_related('reviewer', 'tenant', 'lease')
