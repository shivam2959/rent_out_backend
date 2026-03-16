from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceRequestViewSet

router = DefaultRouter()
router.register(r'requests', MaintenanceRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
