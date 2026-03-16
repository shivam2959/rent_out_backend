from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TenantOnboardingViewSet, MyRoomsView

router = DefaultRouter()
router.register(r'onboarding', TenantOnboardingViewSet, basename='onboarding')
router.register(r'my-rooms', MyRoomsView, basename='my-rooms')

urlpatterns = [
    path('', include(router.urls)),
]
