from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Building, Floor, Room
from .serializers import BuildingSerializer, FloorSerializer, RoomSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'state', 'address']
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        return Building.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FloorViewSet(viewsets.ModelViewSet):
    serializer_class = FloorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Floor.objects.filter(building__owner=self.request.user)

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['room_number', 'room_type']
    ordering_fields = ['rent_amount', 'created_at']

    def get_queryset(self):
        return Room.objects.filter(building__owner=self.request.user)
