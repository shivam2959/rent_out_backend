from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuildingReviewViewSet, TenantReviewViewSet

router = DefaultRouter()
router.register(r'building-reviews', BuildingReviewViewSet)
router.register(r'tenant-reviews', TenantReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
