from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuildingViewSet, RoomViewSet, BuildingPhotoViewSet, RoomPhotoViewSet

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'building-photos', BuildingPhotoViewSet)
router.register(r'room-photos', RoomPhotoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
