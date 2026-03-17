from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VacancyListingViewSet, VacancyApplicationViewSet

router = DefaultRouter()
router.register(r'listings', VacancyListingViewSet, basename='vacancy-listing')
router.register(r'applications', VacancyApplicationViewSet, basename='vacancy-application')

urlpatterns = [
    path('', include(router.urls)),
]
