from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuildingReviewViewSet, TenantReviewViewSet

router = DefaultRouter()
router.register(r'buildings', BuildingReviewViewSet, basename='building-review')
router.register(r'tenants', TenantReviewViewSet, basename='tenant-review')

urlpatterns = [
    path('', include(router.urls)),
]
