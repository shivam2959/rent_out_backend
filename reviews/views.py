from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import BuildingReview, TenantReview
from .serializers import BuildingReviewSerializer, TenantReviewSerializer


class BuildingReviewViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingReviewSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'building__name']
    ordering_fields = ['rating', 'created_at']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = BuildingReview.objects.select_related('reviewer', 'building').all()
        building_id = self.request.query_params.get('building')
        if building_id:
            queryset = queryset.filter(building_id=building_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class TenantReviewViewSet(viewsets.ModelViewSet):
    serializer_class = TenantReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TenantReview.objects.select_related('reviewer', 'tenant', 'building').all()
        tenant_id = self.request.query_params.get('tenant')
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
