from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaseAgreementViewSet

router = DefaultRouter()
router.register(r'agreements', LeaseAgreementViewSet, basename='lease')

urlpatterns = [
    path('', include(router.urls)),
]
