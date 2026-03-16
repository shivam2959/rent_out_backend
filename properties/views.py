from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Building, BuildingPhoto, Room, RoomPhoto
from .serializers import (
    BuildingSerializer, BuildingListSerializer,
    BuildingPhotoSerializer, RoomSerializer, RoomPhotoSerializer
)
from users.permissions import IsOwnerOrAdmin


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.filter(is_active=True).select_related('owner')
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name', 'city', 'state', 'address']
    ordering_fields = ['created_at', 'name', 'city']
    filterset_fields = ['city', 'state', 'building_type']

    def get_serializer_class(self):
        if self.action == 'list':
            return BuildingListSerializer
        return BuildingSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        queryset = Building.objects.filter(is_active=True)
        user = self.request.user
        if not user.is_staff and self.action not in ['list', 'retrieve']:
            queryset = queryset.filter(owner=user)
        return queryset.select_related('owner').prefetch_related('rooms', 'photos')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def available_rooms(self, request, pk=None):
        building = self.get_object()
        rooms = building.rooms.filter(status='available')
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.filter(is_active=True)
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['room_number', 'building__name', 'building__city']
    ordering_fields = ['monthly_rent', 'created_at']
    filterset_fields = ['status', 'room_type', 'furnishing', 'building']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        queryset = Room.objects.filter(is_active=True)
        user = self.request.user
        if not user.is_staff and self.action not in ['list', 'retrieve']:
            queryset = queryset.filter(building__owner=user)
        return queryset.select_related('building')


class BuildingPhotoViewSet(viewsets.ModelViewSet):
    queryset = BuildingPhoto.objects.all()
    serializer_class = BuildingPhotoSerializer
    permission_classes = [IsOwnerOrAdmin]


class RoomPhotoViewSet(viewsets.ModelViewSet):
    queryset = RoomPhoto.objects.all()
    serializer_class = RoomPhotoSerializer
    permission_classes = [IsOwnerOrAdmin]
