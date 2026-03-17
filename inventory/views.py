from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import InventoryItem
from .serializers import InventoryItemSerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category', 'serial_number']
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        user = self.request.user
        if user.role in ('owner', 'admin'):
            return InventoryItem.objects.filter(room__building__owner=user)
        return InventoryItem.objects.filter(
            room__leases__tenant=user, room__leases__status='active'
        ).distinct()
