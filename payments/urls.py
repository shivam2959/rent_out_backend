from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PaymentReceiptViewSet, WebhookView

router = DefaultRouter()
router.register(r'list', PaymentViewSet, basename='payment')
router.register(r'receipts', PaymentReceiptViewSet, basename='receipt')

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='payment-webhook'),
    path('', include(router.urls)),
]
