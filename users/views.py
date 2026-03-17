from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, OwnerProfile, TenantProfile, LeaseOperatorProfile, BrokerProfile, SocietyManagerProfile, BrokerCommission
from .permissions import IsOwner, IsTenant, IsLeaseOperator, IsBroker, IsSocietyManager
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    OwnerProfileSerializer, TenantProfileSerializer, LeaseOperatorProfileSerializer,
    BrokerProfileSerializer, SocietyManagerProfileSerializer, BrokerCommissionSerializer,
)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class OwnerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = OwnerProfileSerializer
    permission_classes = [IsOwner]

    def get_object(self):
        profile, _ = OwnerProfile.objects.get_or_create(user=self.request.user)
        return profile

class TenantProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = TenantProfileSerializer
    permission_classes = [IsTenant]

    def get_object(self):
        profile, _ = TenantProfile.objects.get_or_create(user=self.request.user)
        return profile

    def post(self, request, *args, **kwargs):
        """Submit KYC – marks profile status as 'submitted'."""
        profile, _ = TenantProfile.objects.get_or_create(user=request.user)
        profile.kyc_status = 'submitted'
        profile.save()
        return Response(TenantProfileSerializer(profile).data, status=status.HTTP_200_OK)

class LeaseOperatorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = LeaseOperatorProfileSerializer
    permission_classes = [IsLeaseOperator]

    def get_object(self):
        profile, _ = LeaseOperatorProfile.objects.get_or_create(user=self.request.user)
        return profile

class BrokerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = BrokerProfileSerializer
    permission_classes = [IsBroker]

    def get_object(self):
        profile, _ = BrokerProfile.objects.get_or_create(user=self.request.user)
        return profile

class SocietyManagerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = SocietyManagerProfileSerializer
    permission_classes = [IsSocietyManager]

    def get_object(self):
        profile, _ = SocietyManagerProfile.objects.get_or_create(user=self.request.user)
        return profile


class BrokerCommissionViewSet(viewsets.ModelViewSet):
    """Broker commission management – brokers see their own, owners/admins see all."""
    serializer_class = BrokerCommissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'broker':
            return BrokerCommission.objects.filter(broker=user)
        if user.role == 'owner':
            return BrokerCommission.objects.filter(lease__owner=user)
        return BrokerCommission.objects.all()

    def perform_create(self, serializer):
        serializer.save(broker=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        from django.utils import timezone
        commission = self.get_object()
        commission.status = 'paid'
        commission.paid_at = timezone.now()
        commission.save()
        return Response(BrokerCommissionSerializer(commission).data)
