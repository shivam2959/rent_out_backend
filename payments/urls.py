from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PaymentReceiptViewSet, PaymentGatewayWebhookLogViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'receipts', PaymentReceiptViewSet)
router.register(r'webhooks', PaymentGatewayWebhookLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
