from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaseAgreementViewSet, RentScheduleViewSet

router = DefaultRouter()
router.register(r'list', LeaseAgreementViewSet, basename='lease')
router.register(r'rent-schedules', RentScheduleViewSet, basename='rent-schedule')

urlpatterns = [
    path('', include(router.urls)),
]
