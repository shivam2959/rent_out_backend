from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TenantOnboardingRequestViewSet

router = DefaultRouter()
router.register(r'onboarding', TenantOnboardingRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
