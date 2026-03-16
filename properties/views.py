from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Building, Room, BuildingPhoto, RoomPhoto
from .serializers import (
    BuildingSerializer, BuildingListSerializer,
    RoomSerializer, RoomListSerializer,
    BuildingPhotoSerializer, RoomPhotoSerializer,
)
from users.permissions import IsOwnerOrAdmin


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.select_related('owner').prefetch_related('photos', 'rooms')
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'city', 'state', 'address']
    ordering_fields = ['created_at', 'name', 'city']

    def get_serializer_class(self):
        if self.action == 'list':
            return BuildingListSerializer
        return BuildingSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        queryset = Building.objects.select_related('owner').prefetch_related('photos', 'rooms')
        if self.request.user.role == 'owner' and not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def rooms(self, request, pk=None):
        building = self.get_object()
        rooms = building.rooms.all()
        available = request.query_params.get('available')
        if available is not None:
            rooms = rooms.filter(is_available=available.lower() == 'true')
        serializer = RoomListSerializer(rooms, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def tenants(self, request, pk=None):
        building = self.get_object()
        from django.contrib.auth import get_user_model
        User = get_user_model()
        tenant_ids = building.rooms.filter(
            leases__status='active'
        ).values_list('leases__tenant', flat=True)
        tenants = User.objects.filter(id__in=tenant_ids)
        from users.serializers import UserSerializer
        return Response(UserSerializer(tenants, many=True).data)

    @action(detail=True, methods=['get', 'post'], url_path='photos')
    def photos(self, request, pk=None):
        building = self.get_object()
        if request.method == 'GET':
            photos = building.photos.all()
            return Response(BuildingPhotoSerializer(photos, many=True).data)
        serializer = BuildingPhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(building=building)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['room_number', 'description']
    ordering_fields = ['rent_amount', 'floor', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListSerializer
        return RoomSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        queryset = Room.objects.select_related('building').prefetch_related('photos')
        building_id = self.request.query_params.get('building')
        if building_id:
            queryset = queryset.filter(building_id=building_id)
        available = self.request.query_params.get('available')
        if available is not None:
            queryset = queryset.filter(is_available=available.lower() == 'true')
        room_type = self.request.query_params.get('type')
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        return queryset

    @action(detail=True, methods=['get', 'post'], url_path='photos')
    def photos(self, request, pk=None):
        room = self.get_object()
        if request.method == 'GET':
            photos = room.photos.all()
            return Response(RoomPhotoSerializer(photos, many=True).data)
        serializer = RoomPhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(room=room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
