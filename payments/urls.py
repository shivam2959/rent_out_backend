from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PaymentGatewayWebhookViewSet

router = DefaultRouter()
router.register(r'webhooks', PaymentGatewayWebhookViewSet, basename='webhook')
router.register(r'', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
