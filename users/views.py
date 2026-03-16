from rest_framework import generics, viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import OwnerProfile, TenantProfile, LeaseOperatorProfile
from .serializers import (
    RegisterSerializer, UserSerializer,
    OwnerProfileSerializer, TenantProfileSerializer, LeaseOperatorProfileSerializer
)
from .permissions import IsOwner, IsTenant, IsLeaseOperator

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'email']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OwnerProfileViewSet(viewsets.ModelViewSet):
    queryset = OwnerProfile.objects.all()
    serializer_class = OwnerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OwnerProfile.objects.all()
        return OwnerProfile.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TenantProfileViewSet(viewsets.ModelViewSet):
    queryset = TenantProfile.objects.all()
    serializer_class = TenantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TenantProfile.objects.all()
        return TenantProfile.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LeaseOperatorProfileViewSet(viewsets.ModelViewSet):
    queryset = LeaseOperatorProfile.objects.all()
    serializer_class = LeaseOperatorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LeaseOperatorProfile.objects.all()
        return LeaseOperatorProfile.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
