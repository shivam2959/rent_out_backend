from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceRequestViewSet, MaintenanceCommentViewSet

router = DefaultRouter()
router.register(r'requests', MaintenanceRequestViewSet, basename='maintenance')
router.register(r'comments', MaintenanceCommentViewSet, basename='maintenance-comment')

urlpatterns = [
    path('', include(router.urls)),
]
