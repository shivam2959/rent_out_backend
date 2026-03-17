from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, SubscriptionInvoiceViewSet

router = DefaultRouter()
router.register(r'plans', SubscriptionViewSet, basename='subscription')
router.register(r'invoices', SubscriptionInvoiceViewSet, basename='subscription-invoice')

urlpatterns = [
    path('', include(router.urls)),
]
