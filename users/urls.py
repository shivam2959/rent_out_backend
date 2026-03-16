from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import RegisterView, UserViewSet, OwnerProfileViewSet, TenantProfileViewSet, LeaseOperatorProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'owner-profiles', OwnerProfileViewSet)
router.register(r'tenant-profiles', TenantProfileViewSet)
router.register(r'operator-profiles', LeaseOperatorProfileViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
]
