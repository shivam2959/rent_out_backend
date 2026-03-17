from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PaymentReceiptViewSet, WebhookView, UtilityBillViewSet

router = DefaultRouter()
router.register(r'list', PaymentViewSet, basename='payment')
router.register(r'receipts', PaymentReceiptViewSet, basename='receipt')
router.register(r'utility-bills', UtilityBillViewSet, basename='utility-bill')

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='payment-webhook'),
    path('', include(router.urls)),
]
