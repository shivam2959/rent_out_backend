from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import BuildingReview, TenantReview
from .serializers import BuildingReviewSerializer, TenantReviewSerializer

class BuildingReviewViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BuildingReview.objects.all()

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

class TenantReviewViewSet(viewsets.ModelViewSet):
    serializer_class = TenantReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TenantReview.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
